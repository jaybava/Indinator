"""
Training Script for RL Agent
Automatically plays games to train the reinforcement learning agent.
"""

import json
import random
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from indinator import AkinatorAI


class AutoTrainer:
    """Automatically plays games to train the RL agent."""
    
    def __init__(self):
        """Initialize the trainer."""
        print("🚀 Initializing Auto-Trainer...")
        self.ai = AkinatorAI(
            traits_file="data/traits.json",
            questions_file="data/questions.json",
            characters_file="data/characters.json",
            enable_learning=True
        )
        
        # Load characters
        with open("data/characters.json", 'r') as f:
            self.characters = list(json.load(f).keys())
        
        print(f"✅ Loaded {len(self.characters)} characters")
        print(f"✅ AI Engine ready with {len(self.ai.questions)} questions")
        
        if self.ai.rl_agent:
            stats = self.ai.rl_agent.get_stats()
            print(f"✅ RL Agent initialized (ε={stats['epsilon']:.3f})")
        else:
            print("❌ RL Agent not available!")
            
    def get_character_answer(self, character: str, trait: str) -> bool:
        """
        Get the correct answer for a character's trait.
        
        Args:
            character: Character name
            trait: Trait to check (e.g., "abilities_acrobatics")
            
        Returns:
            True if character has the trait, False otherwise
        """
        if character not in self.ai.traits:
            return False
        
        # Use AI engine's flatten_traits which handles both formats
        char_traits = self.ai.traits[character]
        flat_traits = self.ai._flatten_traits(char_traits)
        
        # Check if trait exists and is positive
        return flat_traits.get(trait, 0) > 0
    
    def play_automated_game(self, character: str, verbose: bool = False) -> dict:
        """
        Play one automated game for a specific character.
        
        Args:
            character: The target character
            verbose: Whether to print detailed progress
            
        Returns:
            Game statistics dict
        """
        self.ai.reset()
        
        questions_asked = 0
        guesses_made = 0
        max_questions = 25
        max_guesses = 3
        
        game_questions = []
        game_traits = []
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"🎯 Target Character: {character}")
            print(f"{'='*60}")
        
        while questions_asked < max_questions and guesses_made < max_guesses:
            # Select best question
            question_idx = self.ai.select_best_question()
            
            if question_idx is None:
                if verbose:
                    print("❌ No more questions available")
                break
            
            question = self.ai.questions[question_idx]
            trait = question.get('trait', '')
            
            # Get correct answer based on character's traits
            answer = self.get_character_answer(character, trait)
            
            if verbose:
                print(f"\nQ{questions_asked + 1}: {question['question']}")
                print(f"   Trait: {trait}")
                print(f"   Answer: {'Yes' if answer else 'No'}")
            
            # Track for RL
            if self.ai.rl_agent:
                entropy_before = self.ai.entropy(self.ai.probabilities)
                top_prob_before = max(self.ai.probabilities)
                remaining_before = len(self.ai.get_remaining_candidates())
                
                rl_state = self.ai.rl_agent.get_state(
                    entropy_before, top_prob_before, questions_asked, remaining_before
                )
                self.ai.rl_agent.record_step(rl_state, trait, -1.0)
            
            # Track question
            game_questions.append(question['question'])
            game_traits.append(trait)
            
            # Update probabilities
            self.ai.update_probabilities(question_idx, answer)
            questions_asked += 1
            
            # Check if we should make a guess
            top_prob = max(self.ai.probabilities)
            top_idx = self.ai.probabilities.index(top_prob)
            top_char = self.ai.characters[top_idx]
            
            # Dynamic confidence threshold
            if questions_asked <= 10:
                threshold = 0.60
            elif questions_asked <= 15:
                threshold = 0.50
            else:
                threshold = 0.40
            
            if top_prob >= threshold:
                guesses_made += 1
                
                if verbose:
                    print(f"\n🤔 Making guess #{guesses_made}: {top_char} ({top_prob*100:.1f}%)")
                
                if top_char == character:
                    # Correct guess!
                    if verbose:
                        print(f"✅ CORRECT! Guessed in {questions_asked} questions")
                    
                    # Log success
                    if self.ai.learner:
                        self.ai.learner.log_game(
                            character=character,
                            questions_asked=game_questions,
                            num_questions=questions_asked,
                            guesses_made=[top_char],
                            success=True,
                            traits_asked=game_traits
                        )
                    
                    if self.ai.rl_agent:
                        self.ai.rl_agent.end_episode(
                            success=True,
                            total_questions=questions_asked
                        )
                    
                    return {
                        'character': character,
                        'success': True,
                        'questions': questions_asked,
                        'guesses': guesses_made,
                        'final_prob': top_prob
                    }
                else:
                    # Wrong guess - penalize and continue
                    if verbose:
                        print(f"❌ Wrong! (Correct: {character})")
                    self.ai.penalize_wrong_guess(top_char)
        
        # Failed to guess correctly
        if verbose:
            print(f"\n❌ FAILED after {questions_asked} questions and {guesses_made} guesses")
            print(f"   Correct answer: {character}")
            # Show top 3 candidates
            indexed_probs = list(enumerate(self.ai.probabilities))
            top_3 = sorted(indexed_probs, key=lambda x: x[1], reverse=True)[:3]
            print(f"   Top guesses:")
            for idx, prob in top_3:
                print(f"     - {self.ai.characters[idx]}: {prob*100:.1f}%")
        
        # Boost correct character for learning
        self.ai.boost_character(character)
        
        # Log failure
        guesses_list = []
        indexed_probs = list(enumerate(self.ai.probabilities))
        top_n = sorted(indexed_probs, key=lambda x: x[1], reverse=True)[:min(3, guesses_made)]
        for idx, prob in top_n:
            guesses_list.append(self.ai.characters[idx])
        
        if self.ai.learner:
            self.ai.learner.log_game(
                character=character,
                questions_asked=game_questions,
                num_questions=questions_asked,
                guesses_made=guesses_list,
                success=False,
                traits_asked=game_traits
            )
        
        if self.ai.rl_agent:
            self.ai.rl_agent.end_episode(
                success=False,
                total_questions=questions_asked
            )
        
        return {
            'character': character,
            'success': False,
            'questions': questions_asked,
            'guesses': guesses_made,
            'final_prob': max(self.ai.probabilities)
        }
    
    def train(self, num_games: int = 100, verbose_interval: int = 10):
        """
        Train the RL agent by playing multiple games.
        
        Args:
            num_games: Number of games to play
            verbose_interval: Show details every N games
        """
        print(f"\n{'='*60}")
        print(f"🎓 Starting Training: {num_games} games")
        print(f"{'='*60}\n")
        
        results = []
        
        for i in range(num_games):
            # Randomly select a character
            character = random.choice(self.characters)
            
            # Play game
            verbose = (i % verbose_interval == 0)
            result = self.play_automated_game(character, verbose=verbose)
            results.append(result)
            
            # Show progress
            if not verbose:
                # Simple progress indicator
                if (i + 1) % 5 == 0:
                    success_rate = sum(1 for r in results if r['success']) / len(results)
                    avg_questions = sum(r['questions'] for r in results) / len(results)
                    print(f"Game {i+1}/{num_games}: "
                          f"Success: {success_rate*100:.1f}%, "
                          f"Avg Questions: {avg_questions:.1f}")
            
            # Show RL progress periodically
            if self.ai.rl_agent and (i + 1) % 20 == 0:
                stats = self.ai.rl_agent.get_stats()
                print(f"\n🤖 RL Progress: {stats['episode_count']} episodes, "
                      f"{stats['unique_states']} states, ε={stats['epsilon']:.3f}\n")
        
        # Final statistics
        print(f"\n{'='*60}")
        print(f"📊 Training Complete!")
        print(f"{'='*60}")
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"\n✅ Success Rate: {len(successful)}/{num_games} ({len(successful)/num_games*100:.1f}%)")
        
        if successful:
            avg_questions_success = sum(r['questions'] for r in successful) / len(successful)
            print(f"   Avg questions (success): {avg_questions_success:.1f}")
        
        if failed:
            avg_questions_fail = sum(r['questions'] for r in failed) / len(failed)
            print(f"   Avg questions (failed): {avg_questions_fail:.1f}")
        
        overall_avg = sum(r['questions'] for r in results) / len(results)
        print(f"   Overall avg questions: {overall_avg:.1f}")
        
        # RL Agent stats
        if self.ai.rl_agent:
            stats = self.ai.rl_agent.get_stats()
            print(f"\n🤖 Final RL Agent State:")
            print(f"   Episodes trained: {stats['episode_count']}")
            print(f"   Unique states learned: {stats['unique_states']}")
            print(f"   Q-table size: {stats['q_table_size']}")
            print(f"   Exploration rate (ε): {stats['epsilon']:.3f}")
        
        # Game history stats
        if self.ai.learner:
            stats = self.ai.learner.get_stats()
            print(f"\n📚 Game History:")
            print(f"   Total games logged: {stats['total_games']}")
            print(f"   Success rate: {stats['success_rate']*100:.1f}%")
            print(f"   Avg questions per game: {stats['avg_questions']:.1f}")
        
        print(f"\n{'='*60}\n")
        
        return results


def main():
    """Main training function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Train the RL agent')
    parser.add_argument('--games', type=int, default=100,
                        help='Number of games to play (default: 100)')
    parser.add_argument('--verbose-interval', type=int, default=10,
                        help='Show details every N games (default: 10)')
    
    args = parser.parse_args()
    
    try:
        trainer = AutoTrainer()
        results = trainer.train(num_games=args.games, verbose_interval=args.verbose_interval)
        
        print("✅ Training completed successfully!")
        print(f"📁 Results saved to:")
        print(f"   - data/game_history.json (game history)")
        print(f"   - data/q_table.json (RL Q-table)")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

