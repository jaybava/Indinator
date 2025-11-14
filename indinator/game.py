"""
CLI Game Interface for Akinator Clone
Handles user interaction and game flow.
"""

from typing import Optional
from .ai_engine import AkinatorAI


class AkinatorGame:
    """Command-line interface for the Akinator game."""
    
    def __init__(self, ai_engine: AkinatorAI):
        """Initialize game with AI engine."""
        self.ai = ai_engine
        self.max_questions = 25
        
        # Track game stats for learning
        self.current_game_questions = []
        self.current_game_traits = []
        self.current_game_guesses = []
        self.current_game_entropy_reductions = []
        self.current_game_rl_states = []  # RL states for each step
        
    def print_header(self):
        """Print game header."""
        print("\n" + "="*60)
        print("  🎭  INDINATOR - AI Character Guessing Game  🎭")
        print("="*60)
        print("\nThink of a character from the list, and I'll try to guess it!")
        print(f"I have {self.ai.num_characters} characters in my database.\n")
    
    def print_divider(self):
        """Print a visual divider."""
        print("-" * 60)
    
    def get_yes_no_input(self, prompt: str) -> Optional[bool]:
        """
        Get yes/no input from user.
        
        Returns:
            True for yes, False for no, None for skip/don't know
        """
        while True:
            response = input(f"{prompt} (yes/no/skip): ").strip().lower()
            
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            elif response in ['s', 'skip', 'idk', "don't know", "dont know"]:
                return None
            elif response in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for playing!")
                return 'quit'
            else:
                print("❌ Please answer 'yes', 'no', or 'skip'")
    
    def show_stats(self):
        """Display current game statistics."""
        stats = self.ai.get_stats()
        
        print(f"\n📊 Current Stats:")
        print(f"   Questions asked: {stats['questions_asked']}/{self.max_questions}")
        print(f"   Remaining candidates: {stats['remaining_candidates']}")
        print(f"   Top guess: {stats['top_character'][0]} ({stats['top_character'][1]*100:.1f}%)")
        
        if stats['remaining_candidates'] <= 10:
            print(f"   Candidates: {', '.join(stats['candidate_names'])}")
    
    def make_guess(self, continue_on_wrong: bool = True) -> bool:
        """
        Make a guess and check if correct.
        
        Args:
            continue_on_wrong: If True, penalize wrong guess and continue game
        
        Returns:
            True if guess was correct, False otherwise
        """
        character, confidence = self.ai.get_best_guess()
        
        self.print_divider()
        print(f"\n🎯 I think I know who it is!\n")
        print(f"   Is your character: {character}?")
        print(f"   (Confidence: {confidence*100:.1f}%)\n")
        
        answer = self.get_yes_no_input("Am I correct?")
        
        if answer == 'quit':
            return 'quit'
        
        if answer:
            print("\n🎉 YES! I guessed it correctly!")
            print(f"✨ It took me {len(self.ai.asked_questions)} questions.\n")
            return (True, character)  # Return success and character
        else:
            print("\n😞 Oh no, I was wrong!")
            
            # Track wrong guess
            self.current_game_guesses.append(character)
            
            # Penalize the wrong guess
            if continue_on_wrong:
                self.ai.penalize_wrong_guess(character, penalty_factor=0.001)  # 99.9% reduction
            
            # Show other top candidates
            top_5 = self.ai.get_top_characters(5)
            if len(top_5) > 0:
                print("\nMy other top guesses are now:")
                for i, (char, prob) in enumerate(top_5[:5], 1):
                    print(f"   {i}. {char} ({prob*100:.1f}%)")
            
            # Ask who it was
            print("\nWho was your character? (This helps me learn!)")
            actual_character = input("Character name: ").strip()
            
            # Try to find with fuzzy matching
            found_char = self.ai.find_character(actual_character)
            
            if found_char:
                print(f"\n💡 Ah! It was {found_char}!")
                if found_char != actual_character:
                    print(f"   (I recognized '{actual_character}' as '{found_char}')")
                
                if continue_on_wrong:
                    # Boost the correct character significantly
                    self.ai.boost_character(found_char, boost_factor=1000.0)
                    print("   Let me continue with this information...")
                else:
                    print("   I'll try to do better next time.")
                
                # Return actual character for logging
                return (False, found_char)
            else:
                print(f"\n🤔 I don't have '{actual_character}' in my database.")
                print("   Similar names I have:")
                # Show suggestions
                suggestions = [c for c in self.ai.characters if any(word in c.lower() for word in actual_character.lower().split())][:5]
                if suggestions:
                    for s in suggestions:
                        print(f"      - {s}")
                else:
                    print("      (No similar characters found)")
            
            return (False, None)
    
    def play_round(self) -> bool:
        """
        Play one round of the game.
        
        Returns:
            True if player wants to play again
        """
        self.ai.reset()
        self.current_game_questions = []
        self.current_game_traits = []
        self.current_game_guesses = []
        self.current_game_entropy_reductions = []
        self.current_game_rl_states = []
        actual_character = None
        game_success = False
        
        self.print_header()
        
        # Ask user to think of a character
        print("📝 Please think of one of the characters in the database.")
        input("   Press Enter when you're ready...")
        
        # Game loop
        questions_asked = 0
        guesses_made = 0
        max_guesses = 3  # Allow up to 3 guesses per game
        
        while questions_asked < self.max_questions:
            # Adjust confidence threshold based on game progress
            # More conservative thresholds to avoid wrong guesses
            if questions_asked <= 8:
                threshold = 0.75  # 75% confidence for early guesses (high bar)
            elif questions_asked <= 12:
                threshold = 0.65  # 65% confidence early-mid game
            elif questions_asked <= 18:
                threshold = 0.55  # 55% confidence mid game
            else:
                threshold = 0.45  # 45% confidence late game
            
            # Check if we should make a guess
            if self.ai.should_make_guess(threshold=threshold) and guesses_made < max_guesses:
                # Get top character
                top_char, top_prob = self.ai.get_best_guess()
                
                # Try to ask a confirmation question first
                confirmation = self.ai.get_confirmation_question(top_char)
                
                if confirmation:
                    question_idx, trait = confirmation
                    question = self.ai.questions[question_idx]
                    
                    self.print_divider()
                    print(f"\n🔍 Confirmation Question:")
                    print(f"❓ {question['question']}")
                    
                    answer = self.get_yes_no_input("\n   Your answer")
                    
                    if answer == 'quit':
                        return False
                    
                    if answer is not None:
                        # Track entropy for confirmation question too
                        entropy_before = self.ai.entropy(self.ai.probabilities)
                        
                        # Track the confirmation question
                        self.current_game_questions.append(question['question'])
                        self.current_game_traits.append(trait)
                        
                        # Update probabilities based on confirmation answer
                        self.ai.update_probabilities(question_idx, answer)
                        
                        # Track entropy reduction
                        entropy_after = self.ai.entropy(self.ai.probabilities)
                        entropy_reduction = entropy_before - entropy_after
                        self.current_game_entropy_reductions.append(entropy_reduction)
                        
                        questions_asked += 1
                        
                        # If answer was NO, dramatically reduce this character's probability
                        if not answer:
                            print(f"\n   ❌ That rules out {top_char}!")
                            self.ai.penalize_wrong_guess(top_char, penalty_factor=0.0001)  # 99.99% reduction
                            
                            # Show updated top candidates
                            new_top = self.ai.get_top_characters(3)
                            print(f"\n   New top candidates:")
                            for i, (char, prob) in enumerate(new_top, 1):
                                print(f"      {i}. {char} ({prob*100:.1f}%)")
                            
                            # Don't make a guess, continue asking questions
                            continue
                        else:
                            print(f"\n   ✅ That's a strong indicator for {top_char}!")
                
                # Now make the actual guess
                result = self.make_guess(continue_on_wrong=True)
                guesses_made += 1
                
                if result == 'quit':
                    return False
                
                # Handle new return format (success, character)
                if isinstance(result, tuple):
                    success, char = result
                    if char and not actual_character:
                        actual_character = char
                    if success:
                        game_success = True
                        break  # Correct guess
                    # Wrong guess, penalized and boosted correct character
                    # Show updated stats
                    print()
                    self.show_stats()
                    
                    # Continue asking more specific questions
                    if questions_asked >= self.max_questions - 2:
                        print("\nI'm running out of questions...")
                        # Make final guess
                        final_result = self.make_guess(continue_on_wrong=False)
                        if final_result == 'quit':
                            return False
                        if isinstance(final_result, tuple):
                            final_success, final_char = final_result
                            if final_char and not actual_character:
                                actual_character = final_char
                            if final_success:
                                game_success = True
                        break
            
            # Select next question
            question_idx = self.ai.select_best_question()
            
            if question_idx is None:
                print("\n🤷 I've run out of questions to ask!")
                self.make_guess()
                break
            
            question = self.ai.questions[question_idx]
            
            # Ask question
            self.print_divider()
            print(f"\nQuestion {questions_asked + 1}/{self.max_questions}:")
            print(f"❓ {question['question']}")
            
            answer = self.get_yes_no_input("\n   Your answer")
            
            if answer == 'quit':
                return False
            
            if answer is None:
                # User skipped, ask different question
                self.ai.asked_questions.add(question_idx)
                continue
            
            # Track entropy BEFORE answering for learning
            entropy_before = self.ai.entropy(self.ai.probabilities)
            top_prob_before = max(self.ai.probabilities)
            remaining_before = len(self.ai.get_remaining_candidates())
            
            # Record RL state-action pair
            if self.ai.enable_learning and self.ai.rl_agent:
                rl_state = self.ai.rl_agent.get_state(
                    entropy_before, top_prob_before, questions_asked, remaining_before
                )
                trait = question.get('trait', '')
                # Record step with -1 reward (cost of asking a question)
                self.ai.rl_agent.record_step(rl_state, trait, -1.0)
                self.current_game_rl_states.append((rl_state, trait))
            
            # Track question and trait for learning
            self.current_game_questions.append(question['question'])
            self.current_game_traits.append(question.get('trait', ''))
            
            # Update probabilities based on answer
            self.ai.update_probabilities(question_idx, answer)
            
            # Track entropy AFTER answering and calculate reduction
            entropy_after = self.ai.entropy(self.ai.probabilities)
            entropy_reduction = entropy_before - entropy_after
            self.current_game_entropy_reductions.append(entropy_reduction)
            
            questions_asked += 1
            
            # Show stats occasionally
            if questions_asked % 5 == 0:
                self.show_stats()
            
            # Check if only one candidate remains
            candidates = self.ai.get_remaining_candidates(min_prob=0.01)
            if len(candidates) == 1:
                print(f"\n💡 Only one candidate remaining!")
                result = self.make_guess()
                if result == 'quit':
                    return False
                break
        else:
            # Max questions reached
            print(f"\n⏰ I've reached my limit of {self.max_questions} questions!")
            self.make_guess()
        
        # Log game for learning (if character was identified)
        if actual_character and self.ai.enable_learning and self.ai.learner:
            try:
                self.ai.learner.log_game(
                    character=actual_character,
                    questions_asked=self.current_game_questions,
                    num_questions=len(self.current_game_questions),
                    guesses_made=self.current_game_guesses,
                    success=game_success,
                    traits_asked=self.current_game_traits,
                    entropy_reductions=self.current_game_entropy_reductions
                )
                
                # Show learning progress after logging
                if game_success:
                    stats = self.ai.learner.get_stats()
                    print(f"\n📈 Learning Progress: {stats['total_games']} games logged, "
                          f"{stats['success_rate']*100:.1f}% success rate")
            except Exception as e:
                print(f"Note: Could not log game: {e}")
        
        # Complete RL episode
        if self.ai.enable_learning and self.ai.rl_agent:
            try:
                self.ai.rl_agent.end_episode(
                    success=game_success,
                    total_questions=len(self.current_game_questions)
                )
                # Show RL learning progress every 10 episodes
                if self.ai.rl_agent.episode_count % 10 == 0:
                    stats = self.ai.rl_agent.get_stats()
                    print(f"\n🤖 RL Agent: {stats['episode_count']} episodes, "
                          f"{stats['unique_states']} states, "
                          f"ε={stats['epsilon']:.3f}")
            except Exception as e:
                print(f"Note: Could not update RL agent: {e}")
        
        # Ask to play again
        self.print_divider()
        play_again = self.get_yes_no_input("\n🎮 Would you like to play again?")
        return play_again == True
    
    def run(self):
        """Main game loop."""
        try:
            while True:
                play_again = self.play_round()
                if not play_again:
                    break
            
            print("\n" + "="*60)
            print("  Thanks for playing INDINATOR!")
            print("  Hope to see you again soon! 👋")
            print("="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Game interrupted. Thanks for playing!")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please report this issue!")

