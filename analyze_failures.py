"""
Analyze AI failures to identify problem characters and patterns.
"""

import json
from collections import defaultdict, Counter

def analyze_game_history():
    """Analyze game history to find patterns in failures."""
    
    with open('data/game_history.json', 'r') as f:
        games = json.load(f)
    
    print("🔍 AI Performance Analysis")
    print("="*60)
    
    # Overall stats
    total = len(games)
    successes = sum(1 for g in games if g.get('success', False))
    failures = total - successes
    
    print(f"\n📊 Overall Performance:")
    print(f"   Total games: {total}")
    print(f"   Successes: {successes} ({successes/total*100:.1f}%)")
    print(f"   Failures: {failures} ({failures/total*100:.1f}%)")
    
    # Failed characters
    failed_characters = defaultdict(int)
    success_characters = defaultdict(int)
    character_questions = defaultdict(list)
    
    for game in games:
        char = game.get('character', 'Unknown')
        success = game.get('success', False)
        num_q = game.get('num_questions', 0)
        
        character_questions[char].append(num_q)
        
        if success:
            success_characters[char] += 1
        else:
            failed_characters[char] += 1
    
    # Find most problematic characters
    if failed_characters:
        print(f"\n❌ Most Difficult Characters (Most Failures):")
        sorted_failures = sorted(failed_characters.items(), key=lambda x: x[1], reverse=True)
        for i, (char, count) in enumerate(sorted_failures[:10], 1):
            total_attempts = failed_characters[char] + success_characters.get(char, 0)
            fail_rate = count / total_attempts * 100 if total_attempts > 0 else 0
            print(f"   {i}. {char}: {count} failures / {total_attempts} attempts ({fail_rate:.1f}% fail rate)")
    
    # Characters that take the most questions
    print(f"\n⏱️  Characters Requiring Most Questions:")
    char_avg_questions = {
        char: sum(qs) / len(qs) 
        for char, qs in character_questions.items() 
        if len(qs) > 0
    }
    sorted_by_questions = sorted(char_avg_questions.items(), key=lambda x: x[1], reverse=True)
    for i, (char, avg_q) in enumerate(sorted_by_questions[:10], 1):
        print(f"   {i}. {char}: {avg_q:.1f} questions average")
    
    # Fastest guesses
    print(f"\n⚡ Easiest Characters (Fewest Questions):")
    sorted_by_speed = sorted(char_avg_questions.items(), key=lambda x: x[1])
    for i, (char, avg_q) in enumerate(sorted_by_speed[:10], 1):
        print(f"   {i}. {char}: {avg_q:.1f} questions average")
    
    # Analyze recent performance (last 50 games)
    recent_games = games[-50:] if len(games) >= 50 else games
    recent_success = sum(1 for g in recent_games if g.get('success', False))
    recent_avg_q = sum(g.get('num_questions', 0) for g in recent_games) / len(recent_games)
    
    print(f"\n📈 Recent Performance (Last {len(recent_games)} Games):")
    print(f"   Success rate: {recent_success/len(recent_games)*100:.1f}%")
    print(f"   Avg questions: {recent_avg_q:.1f}")
    
    # Question efficiency
    success_questions = [g.get('num_questions', 0) for g in games if g.get('success', False)]
    failure_questions = [g.get('num_questions', 0) for g in games if not g.get('success', False)]
    
    if success_questions:
        print(f"\n✅ Successful Games:")
        print(f"   Avg questions: {sum(success_questions)/len(success_questions):.1f}")
        print(f"   Min questions: {min(success_questions)}")
        print(f"   Max questions: {max(success_questions)}")
    
    if failure_questions:
        print(f"\n❌ Failed Games:")
        print(f"   Avg questions: {sum(failure_questions)/len(failure_questions):.1f}")
        print(f"   Min questions: {min(failure_questions)}")
        print(f"   Max questions: {max(failure_questions)}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if failed_characters:
        top_3_failed = sorted_failures[:3]
        print(f"\n   1. Train more on these characters:")
        for char, count in top_3_failed:
            print(f"      - {char}")
        print(f"\n   2. Check if these characters need better traits in traits.json")
        print(f"   3. Run more training: python3 train_ultra.py")
    else:
        print(f"   ✅ No failures detected! AI is performing excellently!")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        analyze_game_history()
    except FileNotFoundError:
        print("❌ Error: game_history.json not found")
        print("Run some games first with: python3 main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

