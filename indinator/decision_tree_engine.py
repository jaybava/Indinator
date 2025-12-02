"""
Decision Tree AI Engine for Akinator Clone
Implements ID3/C4.5 decision tree classifier for optimal question selection.

Methods to implement:
    - __init__()
    - select_best_question()
    - update_state()
    - get_best_guess()
    - should_make_guess()
    - reset()
"""

import json
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from sklearn.tree import DecisionTreeClassifier

# Handle both relative and absolute imports
try:
    from .feature_extractor import FeatureExtractor
except ImportError:
    from indinator.feature_extractor import FeatureExtractor


class DecisionTreeAI:
    """
    Decision Tree AI Engine for character guessing.
    
    Uses scikit-learn's DecisionTreeClassifier to learn optimal question selection
    based on information gain (entropy-based splitting).
    """
    
    def __init__(self, traits_file: str, questions_file: str, characters_file: str = None,
                 max_depth: int = 20, min_samples_split: int = 2):
        """
        Initialize the Decision Tree AI engine.
        
        Args:
            traits_file: Path to traits_flat.json (character -> traits mapping)
            questions_file: Path to questions.json (list of questions)
            characters_file: Path to characters.json (optional, for compatibility)
            max_depth: Maximum depth of the decision tree (default: 20)
            min_samples_split: Minimum samples required to split a node (default: 2)
        """
        # Initialize feature extractor
        print("[INIT] Initializing feature extractor...")
        self.feature_extractor = FeatureExtractor(traits_file, questions_file)
        
        # Load questions for compatibility with existing code
        self.questions = self._load_json(questions_file)
        
        # Get character list
        self.characters = sorted(self.feature_extractor.traits.keys())
        self.num_characters = len(self.characters)
        
        # Build training data
        print("[INIT] Building training data...")
        X, y, character_list = self.feature_extractor.build_feature_matrix()
        
        # Store training data
        self.X_train = X
        self.y_train = y
        self.character_list = character_list
        
        # Train Decision Tree
        print("[INIT] Training Decision Tree...")
        self.tree = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            criterion='entropy',  # Use information gain (ID3/C4.5 style)
            random_state=42  # For reproducibility
        )
        
        self.tree.fit(X, y)
        
        print(f"[OK] Decision Tree trained:")
        print(f"   Depth: {self.tree.get_depth()}")
        print(f"   Leaves: {self.tree.get_n_leaves()}")
        print(f"   Features used: {np.sum(self.tree.feature_importances_ > 0)}")
        
        # Initialize game state (will be reset at start of each game)
        self.reset()
        
        # Cache source traits for redundancy checks (skip asking multiple source questions once one is confirmed)
        self.source_traits = [
            trait for trait in self.feature_extractor.trait_to_index
            if trait.startswith('source_')
        ]
    
    def reset(self):
        """
        Reset the game state for a new game.
        
        Initializes:
        - Current feature vector (all unknown: -1)
        - Known mask (all False)
        - Asked questions set
        - Question history
        - Character probabilities (for compatibility)
        """
        # Create initial feature vector (all unknown)
        self.current_feature_vector = np.full(
            len(self.feature_extractor.feature_names), 
            -1, 
            dtype=np.int8
        )
        
        # Create mask tracking which features are known
        self.known_mask = np.zeros(
            len(self.feature_extractor.feature_names), 
            dtype=bool
        )
        
        # Track asked questions
        self.asked_questions: Set[int] = set()
        self.question_history: List[Dict] = []
        
        # Track answer confidence for each trait (for probabilistic answers)
        # Maps trait_name -> confidence (1.0 for yes/no, 0.75 for probably/probably_not)
        self.answer_confidence: Dict[str, float] = {}
        
        # Character probabilities (for compatibility with existing code)
        # Initialize with uniform distribution
        self.probabilities = [1.0 / self.num_characters] * self.num_characters
    
    def select_best_question(self) -> Optional[int]:
        """
        Select the best next question using the Decision Tree.
        
        Strategy:
        1. For first few questions: Use priority ordering (broad to specific)
        2. Traverse the tree with current known features
        3. When we hit a node that splits on an unknown feature, ask about that feature
        4. If we can't traverse (all needed features unknown), use feature importance
        
        Returns:
            Question index, or None if no more questions available
        """
        questions_asked = len(self.asked_questions)
        
        # Early game: prioritize broad categories by question priority
        if questions_asked < 5:
            priority_question = self._select_priority_question()
            if priority_question is not None:
                return priority_question
        
        # Get tree structure
        tree = self.tree.tree_
        
        # Traverse tree starting from root
        node = 0  # Start at root node
        max_depth = 100  # Prevent infinite loops
        depth = 0
        
        while depth < max_depth:
            depth += 1
            
            # Check if this is a leaf node
            if tree.children_left[node] == tree.children_right[node]:
                # Leaf node reached - this means the tree thinks we've narrowed down enough
                # But we might still have many candidates, so use feature importance instead
                # Don't return None here - use fallback to find a good question
                break
            
            # Get the feature this node splits on
            feature_idx = tree.feature[node]
            
            # Check if this feature is known
            if self.known_mask[feature_idx]:
                # Feature is known - follow the branch
                feature_value = self.current_feature_vector[feature_idx]
                threshold = tree.threshold[node]
                
                # Binary features: 0 or 1, threshold is typically 0.5
                if feature_value <= threshold:
                    node = tree.children_left[node]
                else:
                    node = tree.children_right[node]
            else:
                # Feature is unknown - this is our next question!
                # Map feature index to trait name
                trait_name = self.feature_extractor.index_to_trait[feature_idx]
                
                # Find a question that asks about this trait
                question_indices = self.feature_extractor.trait_to_questions.get(trait_name, [])
                
                # Pick the first question we haven't asked yet and isn't redundant
                for q_idx in question_indices:
                    if q_idx in self.asked_questions:
                        continue
                    if self._is_redundant_question(q_idx):
                        continue
                    return q_idx
                
                # If all questions for this trait were asked, continue traversal
                # (This shouldn't happen, but handle it gracefully)
                # Use feature importance as fallback
                break
        
        # Fallback: Use feature importance to pick best unknown feature
        return self._select_by_feature_importance()
    
    def _select_by_feature_importance(self) -> Optional[int]:
        """
        Select question based on information gain and feature importance.
        
        Uses information gain to pick questions that best split remaining candidates.
        Combines this with feature importance for better question selection.
        
        Returns:
            Question index, or None if no questions available
        """
        # Get feature importances from the tree
        importances = self.tree.feature_importances_
        
        # Find unknown features
        unknown_indices = np.where(~self.known_mask)[0]
        
        if len(unknown_indices) == 0:
            # All features known - should make guess
            return None
        
        # Get top candidates (characters with highest probability)
        # Focus on traits that help distinguish between likely candidates
        top_candidates = self.get_top_characters(10)  # Top 10 candidates
        top_chars = [char for char, _ in top_candidates]
        
        # Calculate information gain for each unknown feature
        scored_features = []
        
        for feature_idx in unknown_indices:
            trait_name = self.feature_extractor.index_to_trait[feature_idx]
            importance = importances[feature_idx]
            
            # Calculate information gain: how well does this trait split top candidates?
            # Count how many top candidates have this trait vs don't
            has_trait = 0
            no_trait = 0
            
            for char in top_chars:
                char_traits = self.feature_extractor.traits.get(char, {})
                if char_traits.get(trait_name, 0) == 1:
                    has_trait += 1
                else:
                    no_trait += 1
            
            # Information gain: prefer traits that split candidates roughly 50/50
            # Perfect split (50/50) = maximum information gain
            total = has_trait + no_trait
            if total == 0:
                info_gain = 0.0
            else:
                # Calculate entropy reduction
                p_yes = has_trait / total
                p_no = no_trait / total
                
                # Entropy: -p*log2(p) - (1-p)*log2(1-p)
                if p_yes > 0 and p_no > 0:
                    entropy = -(p_yes * math.log2(p_yes) + p_no * math.log2(p_no))
                else:
                    entropy = 0.0  # Pure split (all yes or all no) = 0 entropy
                
                # Information gain: higher entropy = better split
                info_gain = entropy
            
            # Combine information gain with feature importance
            # Weight: 70% information gain, 30% feature importance
            combined_score = 0.7 * info_gain + 0.3 * importance
            
            scored_features.append((feature_idx, trait_name, combined_score, info_gain, importance))
        
        # Sort by combined score (highest first)
        scored_features.sort(key=lambda x: x[2], reverse=True)
        
        # Try each feature in order until we find one with an unasked question
        for feature_idx, trait_name, combined_score, info_gain, importance in scored_features:
            # Find a question for this trait
            question_indices = self.feature_extractor.trait_to_questions.get(trait_name, [])
            
            # Pick first unasked, non-redundant question
            for q_idx in question_indices:
                if q_idx in self.asked_questions:
                    continue
                if self._is_redundant_question(q_idx):
                    continue
                return q_idx
        
        # No questions available for any unknown feature
        return None
    
    def _select_priority_question(self) -> Optional[int]:
        """
        Pick next question by lowest priority value, skipping known traits and redundancy.
        Ensures we start with broad categories (source/world/setting/identity/role) before specifics.
        """
        # Build list of candidate questions that are unasked, not redundant, and trait unknown
        candidates = []
        for q_idx, q in enumerate(self.questions):
            if q_idx in self.asked_questions:
                continue
            if self._is_redundant_question(q_idx):
                continue
            trait = q.get('trait', '')
            if not trait:
                continue
            feat_idx = self.feature_extractor.trait_to_index.get(trait, -1)
            if feat_idx >= 0 and self.known_mask[feat_idx]:
                continue
            prio = q.get('priority', 99)
            group = q.get('group', '')
            candidates.append((prio, group, q_idx))
        
        if not candidates:
            return None
        
        # Sort by priority, then by a broadness order for tie-breaking
        broad_order = {
            'source': 0,
            'world': 1,
            'setting': 2,
            'identity': 3,
            'role': 4,
            'affiliation': 5,
            'abilities': 6,
            'appearance': 7,
            'personality': 8
        }
        candidates.sort(key=lambda x: (x[0], broad_order.get(x[1], 9)))
        return candidates[0][2]
    
    def _select_franchise_question(self) -> Optional[int]:
        """
        Select a franchise question for early game (first 1-3 questions).
        
        Prioritizes movie/anime/video_game questions first. If user answers "yes"
        to any of these, we skip asking the others.
        
        Returns:
            Question index for a franchise question, or None if none available
        """
        # Priority franchise questions: movie, anime, video_game
        priority_traits = ['franchise_movie', 'franchise_anime', 'franchise_video_game']
        
        # Check if we've already answered "yes" to any priority question
        # If so, don't ask franchise questions (user already narrowed it down)
        for trait_name in priority_traits:
            if trait_name in self.feature_extractor.trait_to_index:
                feature_idx = self.feature_extractor.trait_to_index[trait_name]
                if self.known_mask[feature_idx]:
                    # This trait is known - check if it's "yes" (value = 1)
                    if self.current_feature_vector[feature_idx] == 1:
                        # User answered yes to one of the priority questions
                        # Skip asking other franchise questions
                        return None
        
        # Find the priority franchise questions (movie, anime, video_game)
        priority_questions = []
        for q_idx, question in enumerate(self.questions):
            if q_idx in self.asked_questions:
                continue
            
            trait_name = question.get('trait', '')
            if trait_name in priority_traits:
                # Check if this trait is still unknown
                if trait_name in self.feature_extractor.trait_to_index:
                    feature_idx = self.feature_extractor.trait_to_index[trait_name]
                    if not self.known_mask[feature_idx]:
                        priority_questions.append((q_idx, trait_name))
        
        # Return the first unasked priority question (in order: movie, anime, video_game)
        if priority_questions:
            # Sort by priority order
            priority_order = {trait: idx for idx, trait in enumerate(priority_traits)}
            priority_questions.sort(key=lambda x: priority_order.get(x[1], 999))
            for q_idx, _ in priority_questions:
                if not self._is_redundant_question(q_idx):
                    return q_idx
        
        # If no priority questions available, fall back to other franchise questions
        # Find all unasked franchise questions
        franchise_questions = []
        
        for q_idx, question in enumerate(self.questions):
            if q_idx in self.asked_questions:
                continue
            
            # Check if this is a franchise question (but not a priority one)
            trait_name = question.get('trait', '')
            if trait_name.startswith('franchise_') and trait_name not in priority_traits:
                # Check if this trait is still unknown
                if trait_name in self.feature_extractor.trait_to_index:
                    feature_idx = self.feature_extractor.trait_to_index[trait_name]
                    if not self.known_mask[feature_idx]:
                        franchise_questions.append(q_idx)
        
        if not franchise_questions:
            return None
        
        # Prioritize by feature importance (most important franchise traits first)
        importances = self.tree.feature_importances_
        
        # Score each franchise question by its trait's importance
        scored_questions = []
        for q_idx in franchise_questions:
            question = self.questions[q_idx]
            trait_name = question.get('trait', '')
            
            # Get feature index for this trait
            if trait_name in self.feature_extractor.trait_to_index:
                feature_idx = self.feature_extractor.trait_to_index[trait_name]
                importance = importances[feature_idx]
                scored_questions.append((q_idx, importance))
        
        if not scored_questions:
            return None
        
        # Sort by importance (highest first) and return the best one
        scored_questions.sort(key=lambda x: x[1], reverse=True)
        for q_idx, _ in scored_questions:
            if not self._is_redundant_question(q_idx):
                return q_idx
        return None

    def _is_redundant_question(self, question_idx: int) -> bool:
        """
        Determine if a question is redundant given already known answers.
        
        Currently skips additional source_* questions once any source_* trait is confirmed yes,
        to avoid wasting turns on mutually exclusive media-origin questions.
        """
        trait = self.feature_extractor.question_to_trait.get(question_idx, '')
        if not trait:
            return False
        
        # Skip redundant source questions if any source is already confirmed yes
        if trait.startswith('source_') and self.source_traits:
            for src_trait in self.source_traits:
                idx = self.feature_extractor.trait_to_index.get(src_trait, -1)
                if idx >= 0 and self.known_mask[idx] and self.current_feature_vector[idx] == 1:
                    return True
        
        # Skip franchise questions that conflict with a confirmed source medium
        if trait.startswith('franchise_'):
            # Map franchises to their primary source medium
            franchise_media = {
                'franchise_star_wars': 'source_movie',
                'franchise_harry_potter': 'source_movie',
                'franchise_lotr': 'source_movie',
                'franchise_marvel': 'source_comic_manga',
                'franchise_dc': 'source_comic_manga',
                'franchise_naruto': 'source_anime',
                'franchise_one_piece': 'source_anime',
                'franchise_dragon_ball': 'source_anime',
                'franchise_pokemon': 'source_anime',
                'franchise_mario': 'source_video_game',
                'franchise_zelda': 'source_video_game',
                'franchise_witcher': 'source_video_game',
                'franchise_halo': 'source_video_game',
                'franchise_got': 'source_tv_streaming',
                'franchise_breaking_bad': 'source_tv_streaming',
                'franchise_stranger_things': 'source_tv_streaming',
                'franchise_pirates': 'source_movie',
                'franchise_matrix': 'source_movie',
                'franchise_incredibles': 'source_movie',
                'franchise_toy_story': 'source_movie',
                'franchise_shrek': 'source_movie',
                'franchise_frozen': 'source_movie',
                'franchise_demon_slayer': 'source_anime',
                'franchise_avatar_tla': 'source_cartoon',
                'franchise_walking_dead': 'source_tv_streaming',
                'franchise_sonic': 'source_video_game',
            }
            needed_source = franchise_media.get(trait)
            if needed_source:
                idx = self.feature_extractor.trait_to_index.get(needed_source, -1)
                if idx >= 0 and self.known_mask[idx]:
                    # If we know the source and it's a mismatch, skip
                    if self.current_feature_vector[idx] != 1:
                        return True
                # Also skip other franchises that don't align once a source is confirmed yes
                for src_trait in self.source_traits:
                    sidx = self.feature_extractor.trait_to_index.get(src_trait, -1)
                    if sidx >= 0 and self.known_mask[sidx] and self.current_feature_vector[sidx] == 1:
                        if src_trait != needed_source:
                            return True
        
        # Skip other franchises once one franchise is confirmed yes
        if trait.startswith('franchise_'):
            for q_idx in self.asked_questions:
                asked_trait = self.feature_extractor.question_to_trait.get(q_idx, '')
                if asked_trait.startswith('franchise_'):
                    a_idx = self.feature_extractor.trait_to_index.get(asked_trait, -1)
                    if a_idx >= 0 and self.known_mask[a_idx] and self.current_feature_vector[a_idx] == 1:
                        # Already confirmed a franchise -> skip other franchises
                        return True
        
        return False
    
    def update_probabilities(self, question_idx: int, user_answer: str,
                            likelihood_correct: float = 0.95, 
                            likelihood_incorrect: float = 0.05):
        """
        Update game state after user answers a question.
        
        This method:
        1. Updates the feature vector with the answer
        2. Updates the known mask
        3. Tracks the question in history
        4. Updates character probabilities based on new information
        
        Args:
            question_idx: Index of the question that was answered
            user_answer: Answer type: "yes", "no", "probably", "probably_not", "dont_know"
            likelihood_correct: Probability user answered correctly (for compatibility)
            likelihood_incorrect: Probability user answered incorrectly (for compatibility)
        """
        # Validate question index
        if question_idx < 0 or question_idx >= len(self.questions):
            # Invalid question index - skip update
            return
        
        # Get question and trait info
        question = self.questions[question_idx]
        trait = question.get('trait', '')
        
        # Handle "don't know" - don't update the feature, just mark question as asked
        if user_answer == "dont_know":
            self.asked_questions.add(question_idx)
            self.question_history.append({
                'question': question.get('question', ''),
                'trait': trait,
                'answer': "don't know"
            })
            # Don't update probabilities for "don't know" answers
            return
        
        # Map answer to confidence level
        answer_confidence_map = {
            "yes": 1.0,
            "no": 1.0,
            "probably": 0.75,  # 75% confident it's yes
            "probably_not": 0.75  # 75% confident it's no
        }
        confidence = answer_confidence_map.get(user_answer, 1.0)
        
        # Store answer confidence for this trait
        if trait:
            self.answer_confidence[trait] = confidence
        
        # Update feature vector using feature extractor
        self.current_feature_vector, self.known_mask = \
            self.feature_extractor.update_feature_vector(
                self.current_feature_vector,
                question_idx,
                user_answer,
                self.known_mask
            )
        
        # Track question in history
        self.asked_questions.add(question_idx)
        
        # Map answer to display string
        answer_display = {
            "yes": "yes",
            "no": "no",
            "probably": "probably",
            "probably_not": "probably not"
        }.get(user_answer, user_answer)
        
        self.question_history.append({
            'question': question.get('question', ''),
            'trait': trait,
            'answer': answer_display
        })
        
        # Update character probabilities
        # Use Decision Tree to predict probabilities based on current known features
        self._update_probabilities_from_tree()
    
    def _update_probabilities_from_tree(self):
        """
        Update character probabilities using a weighted Bayesian-style approach.
        
        Uses a match-counting approach with stronger penalties for mismatches
        to quickly narrow down candidates. The more traits we know, the more
        aggressive we become at eliminating non-matching characters.
        
        For certain answers (yes/no), mismatches are penalized heavily.
        For probabilistic answers (probably/probably_not), mismatches are penalized less.
        """
        # Get known traits from current feature vector
        known_traits = {}
        for i, is_known in enumerate(self.known_mask):
            if is_known:
                trait_name = self.feature_extractor.index_to_trait[i]
                trait_value = int(self.current_feature_vector[i])
                known_traits[trait_name] = trait_value
        
        if not known_traits:
            # No traits known yet - uniform distribution
            self.probabilities = [1.0 / self.num_characters] * self.num_characters
            return
        
        num_known_traits = len(known_traits)
        
        # Hard filters: if a franchise or source trait is confirmed YES, eliminate characters without it
        hard_yes_traits = {
            trait_name for trait_name, val in known_traits.items()
            if val == 1 and (trait_name.startswith('franchise_') or trait_name.startswith('source_'))
        }
        
        # Calculate weighted scores for each character
        # Use multiplicative-style scoring for better discrimination
        character_scores = []
        
        for char in self.characters:
            char_traits = self.feature_extractor.traits.get(char, {})
            match_count = 0
            mismatch_count = 0
            total_weight = 0.0
            
            # Apply hard filter: if char lacks any confirmed franchise/source YES trait, drop to near-zero
            if hard_yes_traits:
                missing_hard = False
                for ht in hard_yes_traits:
                    if char_traits.get(ht, 0) != 1:
                        missing_hard = True
                        break
                if missing_hard:
                    character_scores.append(1e-9)
                    continue
            
            # Count matches and mismatches
            for trait_name, expected_value in known_traits.items():
                char_value = char_traits.get(trait_name, 0)
                confidence = self.answer_confidence.get(trait_name, 1.0)
                
                # Extra weight for franchise/source traits
                if trait_name.startswith('franchise_') or trait_name.startswith('source_'):
                    confidence = max(confidence, 1.2)
                
                weight = confidence
                total_weight += weight
                
                if char_value == expected_value:
                    match_count += 1
                else:
                    mismatch_count += 1
            
            # Calculate score: more matches = higher score, more mismatches = lower score
            # Use a ratio-based approach that becomes more aggressive with more traits
            if num_known_traits == 0:
                score = 1.0
            elif mismatch_count == 0:
                # Perfect match - high score with bonus
                # Bonus increases exponentially with number of matching traits
                # More traits = stronger signal that this is the right character
                score = 1.0 + (match_count * 0.3) + (match_count ** 1.5 * 0.1)  # Exponential bonus
            elif match_count == 0:
                # Complete mismatch - very low score
                # Extremely aggressive penalty: exponential decay
                score = 0.00001 / (3 ** mismatch_count)  # Even heavier penalty
            else:
                # Partial match - use ratio with exponential penalty for mismatches
                match_ratio = match_count / num_known_traits
                
                # More aggressive mismatch penalty (steeper exponential decay)
                mismatch_penalty = 0.25 ** mismatch_count  # Changed from 0.3 to 0.25
                
                # Boost score for high match ratios (characters matching most traits)
                if match_ratio >= 0.9:
                    # Very high match ratio - strong candidate
                    score = match_ratio * mismatch_penalty * 2.0  # Strong bonus
                elif match_ratio >= 0.8:
                    # High match ratio - good candidate
                    score = match_ratio * mismatch_penalty * 1.5  # Moderate bonus
                elif match_ratio >= 0.7:
                    # Decent match ratio
                    score = match_ratio * mismatch_penalty * 1.2  # Small bonus
                else:
                    # Low match ratio - penalize more
                    score = match_ratio * mismatch_penalty * 0.8  # Penalty
            
            # Apply confidence weighting (answers with higher confidence matter more)
            if total_weight > 0:
                # Weight by average confidence of known traits
                avg_confidence = total_weight / num_known_traits
                score *= (0.5 + 0.5 * avg_confidence)  # Scale by confidence
            
            # Apply minimum score but make it very small to allow better discrimination
            character_scores.append(max(0.0001, score))  # Very small minimum to avoid zero
        
        # Normalize scores to probabilities
        total_score = sum(character_scores)
        
        if total_score > 0:
            self.probabilities = [score / total_score for score in character_scores]
        else:
            # Fallback: uniform distribution
            self.probabilities = [1.0 / self.num_characters] * self.num_characters
    
    def get_best_guess(self) -> Tuple[str, float]:
        """
        Get the most likely character based on current probabilities.
        
        Returns:
            Tuple of (character_name, confidence) where confidence is 0-1
        """
        # Find character with highest probability
        max_prob = max(self.probabilities)
        max_idx = self.probabilities.index(max_prob)
        best_character = self.characters[max_idx]
        
        return best_character, max_prob
    
    def get_top_characters(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        Get top N most probable characters.
        
        Args:
            n: Number of top characters to return
            
        Returns:
            List of (character_name, probability) tuples, sorted by probability (descending)
        """
        # Create list of (character, probability) pairs
        char_probs = list(zip(self.characters, self.probabilities))
        
        # Sort by probability (descending)
        char_probs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N
        return char_probs[:n]
    
    def should_make_guess(self, threshold: float = 0.7, max_candidates: int = 5) -> bool:
        """
        Decide if we should make a guess based on confidence threshold and candidate count.
        
        Uses adaptive thresholds: lower threshold when we have fewer candidates,
        higher threshold when we have more candidates.
        
        Args:
            threshold: Base confidence threshold (0-1). If top character's probability
                      exceeds this, we should guess.
            max_candidates: Maximum number of candidates allowed before guessing (default: 3)
                      
        Returns:
            True if we should make a guess, False otherwise
        """
        if not self.probabilities:
            return False
        
        # Get confidence of top character
        max_prob = max(self.probabilities)
        
        questions_asked = len(self.asked_questions)
        
        # Safety check: Don't guess with very low confidence (below 5%)
        # This prevents premature guesses even if candidate count is low
        if max_prob < 0.05:
            return False
        
        # For early questions (<20), only guess if confidence is extremely high (>95%)
        if questions_asked < 20 and max_prob < 0.95:
            return False
        
        # Early stopping: If we have very high confidence (>90%), guess immediately
        # (applies once we're beyond the early-question guard above)
        if max_prob >= 0.90:
            return True
        
        # Check number of remaining candidates
        # Use a higher threshold (0.5%) to only count meaningful candidates
        remaining_candidates = len(self.get_remaining_candidates(min_prob=0.005))

        # Adaptive threshold: lower threshold when fewer candidates
        # More aggressive thresholds to encourage earlier guessing
        if remaining_candidates == 1:
            # Only one candidate - guess if confidence > 15%
            adaptive_threshold = 0.15
        elif remaining_candidates == 2:
            # Two candidates - guess if confidence > 35%
            adaptive_threshold = 0.35
        elif remaining_candidates == 3:
            # Three candidates - use lower threshold (55% instead of base)
            adaptive_threshold = min(threshold, 0.55)
        elif remaining_candidates == 4:
            # Four candidates - use moderate threshold
            adaptive_threshold = min(threshold, 0.60)
        elif remaining_candidates <= 5:
            # Five candidates - use slightly softer base
            adaptive_threshold = min(threshold, 0.70)
        elif remaining_candidates <= 8:
            # 6-8 candidates - modestly higher
            adaptive_threshold = min(0.90, threshold + 0.05)
        else:
            # More than 8 candidates - need higher confidence
            adaptive_threshold = min(0.95, threshold + 0.10)

        # Check if we have too many candidates
        if remaining_candidates > max_candidates and max_prob < adaptive_threshold:
            return False  # Too many candidates with low confidence, don't guess yet

        # Check adaptive confidence threshold
        return bool(max_prob >= adaptive_threshold)
    
    def get_stats(self) -> Dict:
        """
        Get current game statistics.
        
        Returns:
            Dictionary with:
            - 'questions_asked': Number of questions asked
            - 'entropy': Current entropy of probability distribution
            - 'top_character': Tuple of (character_name, probability)
            - 'top_5': List of top 5 (character, probability) tuples
            - 'remaining_candidates': Number of characters still in contention
            - 'candidate_names': List of candidate character names (up to 10)
        """
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
    
    def entropy(self, probabilities: List[float]) -> float:
        """
        Calculate entropy of probability distribution.
        
        Formula: H = -Σ p_i * log2(p_i)
        
        Higher entropy = more uncertainty (more characters still possible)
        Lower entropy = less uncertainty (fewer characters, closer to answer)
        
        Args:
            probabilities: List of probabilities (should sum to 1)
            
        Returns:
            Entropy value in bits (typically 0-7 for 100 characters)
        """
        return -sum(p * math.log2(p) for p in probabilities if p > 1e-10)
    
    def get_remaining_candidates(self, min_prob: float = 0.001) -> List[str]:
        """
        Get characters still in contention (probability above threshold).
        
        Args:
            min_prob: Minimum probability threshold (default: 0.001 = 0.1%)
                     Characters with probability below this are considered eliminated
                     
        Returns:
            List of character names that are still possible
        """
        return [
            char for char, prob in zip(self.characters, self.probabilities)
            if prob >= min_prob
        ]
    
    def find_character(self, name: str) -> Optional[str]:
        """
        Find character with fuzzy name matching.
        
        Tries multiple matching strategies:
        1. Exact match (case-insensitive)
        2. Partial match (substring)
        3. Word match (any word overlap)
        
        Args:
            name: Partial or full character name (e.g., "harry", "Harry Potter", "potter")
            
        Returns:
            Full character name if found, None otherwise
        """
        name_lower = name.lower().strip()
        
        # Exact match first (most reliable)
        for char in self.characters:
            if char.lower() == name_lower:
                return char
        
        # Partial match (substring)
        # Example: "harry" matches "Harry Potter"
        for char in self.characters:
            if name_lower in char.lower() or char.lower() in name_lower:
                return char
        
        # Word match (any word in name)
        # Example: "potter" matches "Harry Potter"
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
                           Lower values = stronger penalty
        """
        if character in self.characters:
            idx = self.characters.index(character)
            self.probabilities[idx] *= penalty_factor
            
            # Normalize probabilities
            total = sum(self.probabilities)
            if total > 0:
                self.probabilities = [p / total for p in self.probabilities]
            else:
                # Fallback: uniform distribution
                self.probabilities = [1.0 / self.num_characters] * self.num_characters
            
            # Only print penalty message in verbose mode (not during benchmarks)
            # This reduces noise during large-scale testing
            # Uncomment the line below if you want to see penalty messages:
            # print(f"   🔻 Reduced probability of {character} by {(1-penalty_factor)*100:.0f}%")
    
    def boost_character(self, character: str, boost_factor: float = 100.0) -> Optional[str]:
        """
        Increase probability of a character (e.g., when user reveals correct answer).
        
        Uses fuzzy matching to find the character, then boosts its probability.
        
        Args:
            character: Name of character to boost (can be partial, e.g., "harry")
            boost_factor: Multiply probability by this factor (default: 100.0 = 100x increase)
            
        Returns:
            Full character name if found, None otherwise
        """
        # Try to find character with fuzzy matching
        found_char = self.find_character(character)
        
        if found_char:
            idx = self.characters.index(found_char)
            self.probabilities[idx] *= boost_factor
            
            # Normalize probabilities
            total = sum(self.probabilities)
            if total > 0:
                self.probabilities = [p / total for p in self.probabilities]
            else:
                # Fallback: uniform distribution
                self.probabilities = [1.0 / self.num_characters] * self.num_characters
            
            print(f"   🔺 Boosted probability of {found_char}")
            return found_char
        
        return None
    
    def get_confirmation_question(self, character: str) -> Optional[Tuple[int, str]]:
        """
        Find the most distinctive trait question for a character to ask as confirmation.
        
        Before making a guess, this finds a question that would strongly confirm
        or rule out the top candidate. Prioritizes traits that distinguish the
        target from other top candidates.
        
        Args:
            character: Character name to find confirmation question for
            
        Returns:
            Tuple of (question_index, trait_name) or None if no good question found
        """
        if character not in self.characters:
            return None
        
        # Get character's traits
        char_traits = self.feature_extractor.traits[character]
        
        # Get top 5 candidates to find discriminating traits
        top_candidates = self.get_top_characters(5)
        top_chars = [char for char, _ in top_candidates]
        
        # Find traits that distinguish the target from other top candidates
        discriminating_traits = []
        
        for trait_name, value in char_traits.items():
            if value == 1:  # Target character has this trait
                # Check how many of the OTHER top candidates also have it
                other_top_with_trait = 0
                for c in top_chars:
                    if c != character:
                        other_traits = self.feature_extractor.traits.get(c, {})
                        if other_traits.get(trait_name, 0) == 1:
                            other_top_with_trait += 1
                
                # Count total characters with this trait (for rarity)
                total_with_trait = sum(
                    1 for c in self.characters
                    if self.feature_extractor.traits.get(c, {}).get(trait_name, 0) == 1
                )
                
                # Prefer traits that:
                # 1. The target has but other top candidates DON'T (high discrimination)
                # 2. Are rare overall (good confirmation)
                if trait_name in self.feature_extractor.trait_to_questions:
                    question_indices = self.feature_extractor.trait_to_questions[trait_name]
                    for q_idx in question_indices:
                        if q_idx not in self.asked_questions:
                            # Score: heavily weight discrimination from top candidates
                            discrimination_score = (len(top_chars) - other_top_with_trait) * 1000
                            rarity_bonus = max(0, (10 - total_with_trait)) * 10
                            total_score = discrimination_score + rarity_bonus
                            
                            discriminating_traits.append((
                                q_idx, trait_name, total_score, other_top_with_trait, total_with_trait
                            ))
        
        # Sort by discrimination score (prefer traits unique among top candidates)
        if discriminating_traits:
            discriminating_traits.sort(key=lambda x: (-x[2], x[3], x[4]))  # High score, low overlap, low total
            return (discriminating_traits[0][0], discriminating_traits[0][1])
        
        return None
    
    def _load_json(self, filepath: str) -> dict:
        """Load JSON file."""
        path = Path(filepath)
        if not path.exists():
            # Try relative to project root
            path = Path(__file__).parent.parent / filepath
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
