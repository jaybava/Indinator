"""
AI Engine for Akinator Clone
Implements Bayesian inference, entropy-based question selection, and PCA embeddings.
"""

import json
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from sklearn.decomposition import PCA

# Import learning system
try:
    from .game_history import GameHistoryLearner
    from .rl_agent import RLQuestionAgent
except ImportError:
    from game_history import GameHistoryLearner
    from rl_agent import RLQuestionAgent


class AkinatorAI:
    """AI engine for character guessing using probabilistic inference with learning."""
    
    def __init__(self, traits_file: str, questions_file: str, characters_file: str, 
                 enable_learning: bool = True):
        """
        Initialize the AI engine.
        
        Args:
            traits_file: Path to traits.json (flat format)
            questions_file: Path to questions.json
            characters_file: Path to characters.json (priors)
            enable_learning: Whether to enable ML learning from game history
        """
        # Load data
        self.traits = self._load_json(traits_file)
        self.questions = self._load_json(questions_file)
        self.priors = self._load_json(characters_file)
        
        # Initialize learning system
        self.enable_learning = enable_learning
        self.learner = None
        self.rl_agent = None
        
        if enable_learning:
            try:
                # Game history learner
                self.learner = GameHistoryLearner()
                # Use adaptive priors if we have enough game history
                adaptive_priors = self.learner.get_adaptive_priors(list(self.traits.keys()))
                if self.learner.get_stats()['total_games'] >= 3:
                    print("📚 Learning from", self.learner.get_stats()['total_games'], "past games...")
                    self.priors = adaptive_priors
                
                # RL agent for question selection
                self.rl_agent = RLQuestionAgent()
                rl_stats = self.rl_agent.get_stats()
                if rl_stats['learning_active']:
                    print(f"🤖 RL Agent trained on {rl_stats['episode_count']} episodes "
                          f"({rl_stats['unique_states']} states learned)")
                    
            except Exception as e:
                print(f"Note: Learning system not available: {e}")
                self.learner = None
                self.rl_agent = None
                self.enable_learning = False
        
        # Get character list
        self.characters = list(self.traits.keys())
        self.num_characters = len(self.characters)
        
        # Initialize probabilities with priors
        self.probabilities = [self.priors.get(char, 0.01) for char in self.characters]
        self._normalize_probabilities()
        
        # Track asked questions
        self.asked_questions = set()
        self.question_history = []
        
        # Create embeddings using PCA
        self.embeddings = self._create_embeddings()
        
        # Index questions by trait for fast lookup
        self.trait_to_questions = self._index_questions_by_trait()
        
    def _load_json(self, filepath: str) -> dict:
        """Load JSON file."""
        path = Path(filepath)
        if not path.exists():
            # Try relative to project root
            path = Path(__file__).parent.parent / filepath
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _normalize_probabilities(self):
        """Normalize probabilities to sum to 1."""
        total = sum(self.probabilities)
        if total > 0:
            self.probabilities = [p / total for p in self.probabilities]
        else:
            # Reset to uniform if all became zero
            self.probabilities = [1.0 / self.num_characters] * self.num_characters
    
    def _flatten_traits(self, nested_traits: Dict) -> Dict[str, float]:
        """
        Flatten nested trait structure with group prefixes.
        
        Args:
            nested_traits: Nested dict like {"identity": {"gender_m": 1}}
            
        Returns:
            Flat dict like {"identity_gender_m": 1} AND {"gender_m": 1}
            (includes both prefixed and non-prefixed versions for compatibility)
        """
        flat = {}
        for group, traits in nested_traits.items():
            if isinstance(traits, dict):
                # Add both with and without prefix for maximum compatibility
                for trait_name, value in traits.items():
                    # With prefix (matches questions.json format)
                    prefixed_name = f"{group}_{trait_name}"
                    flat[prefixed_name] = value
                    # Without prefix (for backward compatibility)
                    flat[trait_name] = value
            else:
                # Handle non-nested case
                flat[group] = traits
        return flat
    
    def _create_embeddings(self) -> Dict[str, np.ndarray]:
        """
        Create PCA embeddings for all characters.
        Reduces high-dimensional trait space to lower dimensions.
        """
        # Flatten all traits first
        flat_traits = {}
        for char, nested_traits in self.traits.items():
            flat_traits[char] = self._flatten_traits(nested_traits)
        
        # Create trait matrix
        all_traits = set()
        for char_flat_traits in flat_traits.values():
            all_traits.update(char_flat_traits.keys())
        
        trait_list = sorted(all_traits)
        
        # Build matrix: rows = characters, cols = traits
        matrix = []
        for char in self.characters:
            char_vector = [flat_traits[char].get(trait, 0) for trait in trait_list]
            matrix.append(char_vector)
        
        X = np.array(matrix)
        
        # Apply PCA to reduce dimensionality
        n_components = min(16, X.shape[0], X.shape[1])  # 16D or less
        pca = PCA(n_components=n_components)
        embeddings_array = pca.fit_transform(X)
        
        # Store as dict
        embeddings = {
            self.characters[i]: embeddings_array[i] 
            for i in range(len(self.characters))
        }
        
        print(f"✓ Created {n_components}-dimensional embeddings for {len(self.characters)} characters")
        return embeddings
    
    def _index_questions_by_trait(self) -> Dict[str, List[int]]:
        """Create an index mapping traits to question indices."""
        trait_index = {}
        for i, q in enumerate(self.questions):
            trait = q.get('trait', '')
            if trait not in trait_index:
                trait_index[trait] = []
            trait_index[trait].append(i)
        return trait_index
    
    def entropy(self, probabilities: List[float]) -> float:
        """
        Calculate entropy of probability distribution.
        H = -Σ p_i * log2(p_i)
        
        Higher entropy = more uncertainty
        """
        return -sum(p * math.log2(p) for p in probabilities if p > 1e-10)
    
    def expected_information_gain(self, question_idx: int) -> float:
        """
        Calculate expected information gain for a question.
        
        IG(Q) = H(before) - E[H(after)]
        
        This tells us how much uncertainty the question reduces on average.
        """
        question = self.questions[question_idx]
        trait = question.get('trait', '')
        
        # Current entropy
        H_before = self.entropy(self.probabilities)
        
        # Split characters by whether they have this trait
        yes_probs = []
        no_probs = []
        
        for i, char in enumerate(self.characters):
            char_traits = self.traits[char]
            flat_traits = self._flatten_traits(char_traits)
            has_trait = flat_traits.get(trait, 0) == 1
            
            if has_trait:
                yes_probs.append(self.probabilities[i])
                no_probs.append(0.0)
            else:
                yes_probs.append(0.0)
                no_probs.append(self.probabilities[i])
        
        # Calculate probability of each answer
        P_yes = sum(yes_probs)
        P_no = sum(no_probs)
        
        # Calculate entropy after each answer
        H_yes = 0.0
        if P_yes > 1e-10:
            normalized_yes = [p / P_yes for p in yes_probs if p > 1e-10]
            H_yes = self.entropy(normalized_yes)
        
        H_no = 0.0
        if P_no > 1e-10:
            normalized_no = [p / P_no for p in no_probs if p > 1e-10]
            H_no = self.entropy(normalized_no)
        
        # Expected entropy after asking
        H_after = P_yes * H_yes + P_no * H_no
        
        # Information gain
        return H_before - H_after
    
    def select_best_question(self, focus_top_n: int = 10) -> Optional[int]:
        """
        Select the question with highest information gain.
        This is the core AI decision-making with strategic prioritization.
        
        Args:
            focus_top_n: Consider traits that discriminate among top N candidates
        """
        best_idx = None
        best_gain = -1.0
        
        # Get top candidates
        top_candidates = self.get_top_characters(focus_top_n)
        top_chars = [char for char, _ in top_candidates]
        
        # Find traits that differ among top candidates
        discriminating_traits = set()
        if len(top_chars) > 1:
            for trait in self.trait_to_questions.keys():
                # Check if this trait varies among top candidates
                values = [self._flatten_traits(self.traits[char]).get(trait, 0) for char in top_chars]
                if len(set(values)) > 1:  # Trait has different values
                    discriminating_traits.add(trait)
        
        # Strategic question prioritization based on game state
        asked_traits = [self.questions[i].get('trait', '') for i in self.asked_questions]
        num_asked = len(self.asked_questions)
        
        # Phase 1: Early game (0-3 questions) - establish broad categories
        priority_traits = set()
        if num_asked <= 3:
            # Prioritize franchise/media type questions
            priority_traits = {t for t in self.trait_to_questions.keys() 
                             if t in ['franchise_anime', 'franchise_video_game', 
                                     'franchise_tv_show', 'franchise_movie',
                                     'franchise_nintendo', 'franchise_disney']}
        
        # Phase 2: After media type known (4-8 questions) - narrow to specific franchise
        elif num_asked <= 8:
            # If anime is confirmed, prioritize major anime franchises AND colors
            if 'franchise_anime' in asked_traits:
                # Count how many anime franchises we've already asked about
                anime_franchises_asked = [t for t in asked_traits if t.startswith('franchise_franchise_')]
                
                # If we've asked about 2+ franchises without finding it, SWITCH to visual traits
                if len(anime_franchises_asked) >= 2:
                    # Prioritize distinctive colors which are HIGHLY discriminating
                    priority_traits = {t for t in self.trait_to_questions.keys()
                                     if t in ['appearance_color_orange', 'appearance_color_yellow',
                                             'appearance_color_green', 'appearance_color_pink',
                                             'appearance_hair_orange', 'appearance_hair_green',
                                             'appearance_hair_pink', 'appearance_has_headband',
                                             'appearance_has_hat', 'appearance_spiky_hair']}
                else:
                    # Ask about major anime franchises systematically
                    # Define all major anime franchises
                    major_anime_franchises = [
                        'franchise_franchise_naruto',
                        'franchise_franchise_one_piece', 
                        'franchise_franchise_dragon_ball',
                        'franchise_franchise_pokemon',
                        'franchise_franchise_death_note',
                        'franchise_franchise_aot'
                    ]
                    
                    # Check which franchises we've already asked about
                    asked_anime_franchises = [t for t in asked_traits if t in major_anime_franchises]
                    
                    # Check which franchises the top candidates belong to
                    top_char_franchises = set()
                    for char, _ in top_candidates[:10]:  # Check top 10 instead of 5
                        char_traits = self.traits[char]
                        flat_traits = self._flatten_traits(char_traits)
                        for franchise in major_anime_franchises:
                            if franchise not in asked_anime_franchises and flat_traits.get(franchise, 0) == 1:
                                top_char_franchises.add(franchise)
                    
                    # Prioritize franchises that top candidates belong to
                    if top_char_franchises:
                        priority_traits = top_char_franchises
                    else:
                        # Ask about remaining unasked major anime franchises
                        priority_traits = {t for t in major_anime_franchises if t not in asked_anime_franchises}
                        
                        # If we've asked about all major franchises, switch to colors/appearance
                        if not priority_traits:
                            priority_traits = {t for t in self.trait_to_questions.keys()
                                             if t.startswith('appearance_color_') or 
                                                t.startswith('appearance_hair_')}
            
            # If video game confirmed, ask which game franchise
            elif 'franchise_video_game' in asked_traits:
                priority_traits = {t for t in self.trait_to_questions.keys() 
                                 if t.startswith('franchise_franchise_') and
                                 any(game in t for game in ['mario', 'zelda', 'halo', 'witcher', 
                                                            'god_of_war', 'tlou'])}
            
            # Always include highly distinctive visual traits as backup
            priority_traits |= {t for t in discriminating_traits 
                              if (t.startswith('appearance_color_') or 
                                  'distinctive' in t)}
        
        # Phase 3: Late game - focus on unique abilities and specific traits
        else:
            priority_traits = {t for t in discriminating_traits 
                             if (t.startswith('abilities_') or 
                                 t.startswith('appearance_has_') or
                                 'distinctive' in t)}
        
        # Evaluate all unasked questions
        candidates = []
        for i in range(len(self.questions)):
            if i in self.asked_questions:
                continue
            
            gain = self.expected_information_gain(i)
            trait = self.questions[i].get('trait', '')
            
            # Count how many characters have this trait
            char_count = sum(self._flatten_traits(self.traits[char]).get(trait, 0) for char in self.characters)
            
            # MAJOR boost for priority traits based on game phase
            if trait in priority_traits:
                # MASSIVE boost for franchise questions early game
                if trait.startswith('franchise_franchise_') and num_asked <= 10:
                    gain *= 5.0  # 5x multiplier for franchise questions
                # Extra boost for distinctive color traits (very discriminating)
                elif trait.startswith('appearance_color_') or trait.startswith('appearance_hair_'):
                    gain *= 4.0  # 4x multiplier for color questions
                else:
                    gain *= 3.0  # 3x multiplier for other strategic priority
            
            # Boost score if this question discriminates top candidates
            if trait in discriminating_traits:
                gain *= 1.8  # 80% bonus for discriminating questions
            
            # Massive boost for ultra-rare traits (only 1-2 characters have it)
            if char_count == 1:
                gain *= 3.0  # Unique trait - MASSIVE boost
            elif char_count == 2:
                gain *= 2.5  # Very rare trait
            elif char_count <= 3:
                gain *= 2.0  # Rare trait
            elif char_count <= 5:
                gain *= 1.5  # Uncommon trait
            
            # Penalize very common traits (most characters have it)
            if char_count > len(self.characters) * 0.7:
                gain *= 0.5  # Common trait - reduce priority
            
            # Penalize generic personality traits early in the game
            if num_asked < 8 and trait.startswith('personality_'):
                if trait not in discriminating_traits:
                    gain *= 0.3  # Heavy penalty for generic personality questions
            
            # Apply learned boost from game history (entropy-based)
            if self.enable_learning and self.learner:
                learned_boost = self.learner.get_question_boost(trait)
                gain *= learned_boost
            
            # Apply RL agent Q-value boost
            if self.enable_learning and self.rl_agent:
                # Get current state
                current_entropy = self.entropy(self.probabilities)
                top_prob = max(self.probabilities)
                remaining = len(self.get_remaining_candidates())
                state = self.rl_agent.get_state(current_entropy, top_prob, num_asked, remaining)
                
                # Get Q-value for this action
                q_value = self.rl_agent.get_action_value(state, trait)
                
                # Convert Q-value to boost (Q-values can be negative)
                # Good actions have positive Q, bad actions have negative Q
                # Map to boost range: Q=-50 -> 0.5x, Q=0 -> 1.0x, Q=50 -> 1.5x
                rl_boost = 1.0 + (q_value / 100.0)
                rl_boost = max(0.5, min(2.0, rl_boost))  # Clamp to reasonable range
                
                gain *= rl_boost
            
            candidates.append((i, gain))
        
        # Sort by gain and pick best
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            best_idx = candidates[0][0]
        
        return best_idx
    
    def update_probabilities(self, question_idx: int, user_answer: bool, 
                            likelihood_correct: float = 0.95, likelihood_incorrect: float = 0.05):
        """
        Update character probabilities using Bayesian inference.
        
        P(char | answer) ∝ P(answer | char) * P(char)
        
        Args:
            question_idx: Index of the question answered
            user_answer: True for yes, False for no
            likelihood_correct: P(answer=yes | trait=yes) - higher = more confident
            likelihood_incorrect: P(answer=yes | trait=no) - lower = more penalty
        """
        question = self.questions[question_idx]
        trait = question.get('trait', '')
        
        # Update probabilities based on answer
        new_probs = []
        for i, char in enumerate(self.characters):
            char_traits = self.traits[char]
            # Flatten nested traits
            flat_traits = self._flatten_traits(char_traits)
            has_trait = flat_traits.get(trait, 0) == 1
            
            # Likelihood: probability of user's answer given character
            if user_answer:
                # User said yes
                likelihood = likelihood_correct if has_trait else likelihood_incorrect
            else:
                # User said no
                likelihood = likelihood_correct if not has_trait else likelihood_incorrect
            
            # Bayesian update
            new_probs.append(self.probabilities[i] * likelihood)
        
        self.probabilities = new_probs
        self._normalize_probabilities()
        
        # Track question
        self.asked_questions.add(question_idx)
        self.question_history.append({
            'question': question['question'],
            'trait': trait,
            'answer': 'yes' if user_answer else 'no'
        })
    
    def get_top_characters(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        Get top N most probable characters.
        
        Returns:
            List of (character_name, probability) tuples
        """
        char_probs = list(zip(self.characters, self.probabilities))
        char_probs.sort(key=lambda x: x[1], reverse=True)
        return char_probs[:n]
    
    def get_best_guess(self) -> Tuple[str, float]:
        """Get the single most likely character."""
        best_idx = max(range(len(self.probabilities)), key=lambda i: self.probabilities[i])
        return self.characters[best_idx], self.probabilities[best_idx]
    
    def should_make_guess(self, threshold: float = 0.7) -> bool:
        """
        Decide if we should make a guess.
        
        Args:
            threshold: Confidence threshold (0-1)
        
        Returns:
            True if top character exceeds threshold
        """
        max_prob = max(self.probabilities)
        return max_prob >= threshold
    
    def get_remaining_candidates(self, min_prob: float = 0.001) -> List[str]:
        """Get characters still in contention."""
        return [
            char for char, prob in zip(self.characters, self.probabilities)
            if prob >= min_prob
        ]
    
    def find_character(self, name: str) -> Optional[str]:
        """
        Find character with fuzzy name matching.
        
        Args:
            name: Partial or full character name
            
        Returns:
            Full character name if found, None otherwise
        """
        name_lower = name.lower().strip()
        
        # Exact match first
        for char in self.characters:
            if char.lower() == name_lower:
                return char
        
        # Partial match (substring)
        for char in self.characters:
            if name_lower in char.lower() or char.lower() in name_lower:
                return char
        
        # Word match (any word in name)
        name_words = set(name_lower.split())
        for char in self.characters:
            char_words = set(char.lower().split())
            if name_words & char_words:  # Any word overlap
                return char
        
        return None
    
    def penalize_wrong_guess(self, character: str, penalty_factor: float = 0.01):
        """
        Drastically reduce probability of a character after wrong guess.
        
        Args:
            character: Name of character that was guessed incorrectly
            penalty_factor: Multiply probability by this factor (0.01 = 99% reduction)
        """
        if character in self.characters:
            idx = self.characters.index(character)
            self.probabilities[idx] *= penalty_factor
            self._normalize_probabilities()
            print(f"   🔻 Reduced probability of {character} by {(1-penalty_factor)*100:.0f}%")
    
    def boost_character(self, character: str, boost_factor: float = 100.0):
        """
        Increase probability of a character (e.g., when user reveals answer).
        
        Args:
            character: Name of character to boost (can be partial)
            boost_factor: Multiply probability by this factor
        """
        # Try to find character with fuzzy matching
        found_char = self.find_character(character)
        
        if found_char:
            idx = self.characters.index(found_char)
            self.probabilities[idx] *= boost_factor
            self._normalize_probabilities()
            print(f"   🔺 Boosted probability of {found_char}")
            return found_char
        
        return None
    
    def reset(self):
        """Reset the game state."""
        self.probabilities = [self.priors.get(char, 0.01) for char in self.characters]
        self._normalize_probabilities()
        self.asked_questions = set()
        self.question_history = []
    
    def get_confirmation_question(self, character: str) -> Optional[Tuple[int, str]]:
        """
        Find the most distinctive trait question for a character to ask as confirmation.
        Prioritizes traits that distinguish the target from other top candidates.
        
        Args:
            character: Character name to find confirmation question for
            
        Returns:
            Tuple of (question_index, trait_name) or None if no good question found
        """
        if character not in self.characters:
            return None
        
        char_traits = self.traits[character]
        flat_traits = self._flatten_traits(char_traits)
        
        # Get top 5 candidates to find discriminating traits
        top_candidates = self.get_top_characters(5)
        top_chars = [char for char, _ in top_candidates]
        
        # Find traits that distinguish the target from other top candidates
        discriminating_traits = []
        
        for trait, value in flat_traits.items():
            if value == 1:  # Target has this trait
                # Check how many of the OTHER top candidates also have it
                other_top_with_trait = sum(
                    1 for c in top_chars 
                    if c != character and self._flatten_traits(self.traits[c]).get(trait, 0) == 1
                )
                
                # Count total characters with this trait (for rarity)
                total_with_trait = sum(self._flatten_traits(self.traits[c]).get(trait, 0) for c in self.characters)
                
                # Prefer traits that:
                # 1. The target has but other top candidates DON'T (high discrimination)
                # 2. Are rare overall (good confirmation)
                if trait in self.trait_to_questions:
                    question_indices = self.trait_to_questions[trait]
                    for q_idx in question_indices:
                        if q_idx not in self.asked_questions:
                            # Score: heavily weight discrimination from top candidates
                            discrimination_score = (len(top_chars) - other_top_with_trait) * 1000
                            rarity_bonus = max(0, (10 - total_with_trait)) * 10
                            total_score = discrimination_score + rarity_bonus
                            
                            discriminating_traits.append((
                                q_idx, trait, total_score, other_top_with_trait, total_with_trait
                            ))
        
        # Sort by discrimination score (prefer traits unique among top candidates)
        if discriminating_traits:
            discriminating_traits.sort(key=lambda x: (-x[2], x[3], x[4]))  # High score, low overlap, low total
            return (discriminating_traits[0][0], discriminating_traits[0][1])
        
        return None
    
    def get_stats(self) -> Dict:
        """Get current game statistics."""
        top_5 = self.get_top_characters(5)
        candidates = self.get_remaining_candidates()
        
        return {
            'questions_asked': len(self.asked_questions),
            'entropy': self.entropy(self.probabilities),
            'top_character': top_5[0] if top_5 else ('Unknown', 0.0),
            'top_5': top_5,
            'remaining_candidates': len(candidates),
            'candidate_names': candidates[:10]  # Show up to 10
        }

