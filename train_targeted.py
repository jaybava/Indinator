"""
Targeted training - focuses on characters the AI struggles with.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

from scripts.train_rl_agent import AutoTrainer

def get_problem_characters(top_n=20):
    """Identify characters with highest failure rates."""
    try:
        with open('data/game_history.json', 'r') as f:
            games = json.load(f)
    except FileNotFoundError:
        print("No game history found. Using all characters.")
        with open('data/characters.json', 'r') as f:
            return list(json.load(f).keys())
    
    failed_chars = defaultdict(int)
    success_chars = defaultdict(int)
    
    for game in games:
        char = game.get('character', 'Unknown')
        if game.get('success', False):
            success_chars[char] += 1
        else:
            failed_chars[char] += 1
    
    # Calculate failure rates
    problem_chars = []
    for char in failed_chars:
        total = failed_chars[char] + success_chars.get(char, 0)
        fail_rate = failed_chars[char] / total if total > 0 else 0
        problem_chars.append((char, fail_rate, failed_chars[char], total))
    
    # Sort by failure rate, then by total failures
    problem_chars.sort(key=lambda x: (x[1], x[2]), reverse=True)
    
    return [char for char, _, _, _ in problem_chars[:top_n]]

def targeted_training(num_games=200):
    """Train specifically on problem characters."""
    
    print("🎯 INDINATOR - Targeted Training Mode")
    print("="*60)
    
    # Identify problem characters
    problem_chars = get_problem_characters(top_n=30)
    
    if not problem_chars:
        print("No problem characters identified.")
        print("Using all characters for training.")
        with open('data/characters.json', 'r') as f:
            problem_chars = list(json.load(f).keys())
    else:
        print(f"Identified {len(problem_chars)} characters needing more training:")
        for i, char in enumerate(problem_chars[:10], 1):
            print(f"   {i}. {char}")
        if len(problem_chars) > 10:
            print(f"   ... and {len(problem_chars)-10} more")
    
    print(f"\nThis will train on these characters for {num_games} games.")
    print("="*60 + "\n")
    
    response = input("Start targeted training? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("Training cancelled.")
        return
    
    try:
        trainer = AutoTrainer()
        
        print(f"\n🎯 Training on {len(problem_chars)} problem characters...")
        print(f"{'='*60}\n")
        
        results = []
        
        for i in range(num_games):
            # Pick from problem characters more frequently
            import random
            if random.random() < 0.8:  # 80% from problem chars
                char = random.choice(problem_chars)
            else:  # 20% from all chars
                char = random.choice(trainer.characters)
            
            verbose = (i % 25 == 0)
            result = trainer.play_automated_game(char, verbose=verbose)
            results.append(result)
            
            # Progress update
            if (i + 1) % 25 == 0:
                recent = results[-25:]
                success_rate = sum(1 for r in recent if r['success']) / len(recent)
                avg_questions = sum(r['questions'] for r in recent) / len(recent)
                print(f"Game {i+1}/{num_games}: Success: {success_rate*100:.1f}%, Avg Q: {avg_questions:.1f}")
        
        # Final stats
        print("\n" + "="*60)
        print("🎯 Targeted Training Complete!")
        print("="*60)
        
        successful = [r for r in results if r['success']]
        print(f"\n✅ Success Rate: {len(successful)}/{num_games} ({len(successful)/num_games*100:.1f}%)")
        
        if successful:
            avg_q = sum(r['questions'] for r in successful) / len(successful)
            print(f"⚡ Avg Questions (success): {avg_q:.1f}")
        
        if trainer.ai.rl_agent:
            stats = trainer.ai.rl_agent.get_stats()
            print(f"\n🤖 RL Agent:")
            print(f"   States: {stats['unique_states']}")
            print(f"   Q-values: {stats['q_table_size']}")
        
        print("\n💡 Recommendation: Test the AI now with: python3 main.py")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Training interrupted!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    targeted_training(num_games=200)

