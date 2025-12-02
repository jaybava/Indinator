"""
Feature Extraction for Decision Tree
Converts character traits to feature vectors for training and inference.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Set, Tuple


class FeatureExtractor:
    """
    Extracts features from character traits for Decision Tree training and inference.
    
    Each character is represented as a binary feature vector where:
    - Each feature corresponds to a trait (e.g., "abilities_magic", "appearance_has_glasses")
    - Value 1 = character has the trait, 0 = character doesn't have it
    """
    
    def __init__(self, traits_file: str, questions_file: str):
        """
        Initialize the feature extractor.
        
        Args:
            traits_file: Path to traits_flat.json (character -> traits mapping)
            questions_file: Path to questions.json (list of questions with trait names)
        """
        # Load data files
        self.traits = self._load_json(traits_file)
        self.questions = self._load_json(questions_file)
        
        # Get all unique trait names across all characters
        # This creates our feature space (one feature per trait)
        all_traits = set()
        for character_traits in self.traits.values():
            all_traits.update(character_traits.keys())
        
        # Sort traits for consistent ordering (important for feature indices)
        self.feature_names = sorted(all_traits)
        
        # Create mapping: trait_name -> feature_index
        # Example: "abilities_magic" -> 42
        self.trait_to_index = {trait: idx for idx, trait in enumerate(self.feature_names)}
        
        # Create reverse mapping: feature_index -> trait_name
        self.index_to_trait = {idx: trait for trait, idx in self.trait_to_index.items()}
        
        # Create mapping: question_index -> trait_name
        # This lets us know which trait a question asks about
        self.question_to_trait = {}
        for q_idx, question in enumerate(self.questions):
            trait = question.get('trait', '')
            if trait:
                self.question_to_trait[q_idx] = trait
        
        # Create reverse mapping: trait_name -> list of question_indices
        # (Some traits might have multiple questions)
        self.trait_to_questions = {}
        for q_idx, question in enumerate(self.questions):
            trait = question.get('trait', '')
            if trait:
                if trait not in self.trait_to_questions:
                    self.trait_to_questions[trait] = []
                self.trait_to_questions[trait].append(q_idx)
        
        print(f"[OK] Feature extractor initialized:")
        print(f"   Characters: {len(self.traits)}")
        print(f"   Features (traits): {len(self.feature_names)}")
        print(f"   Questions: {len(self.questions)}")
    
    def build_feature_matrix(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Build the feature matrix for Decision Tree training.
        
        Creates a matrix where:
        - Each row = one character
        - Each column = one trait (feature)
        - Value = 1 if character has trait, 0 if not
        
        Returns:
            X: Feature matrix (n_characters × n_features) - binary values
            y: Labels array (n_characters) - character names
            character_list: List of character names in same order as rows
        """
        # Get list of characters (sorted for consistency)
        character_list = sorted(self.traits.keys())
        n_characters = len(character_list)
        n_features = len(self.feature_names)
        
        # Initialize feature matrix with zeros
        # Shape: (n_characters, n_features)
        X = np.zeros((n_characters, n_features), dtype=np.int8)
        
        # Fill in the matrix
        for char_idx, character in enumerate(character_list):
            character_traits = self.traits[character]
            
            # For each trait this character has, set corresponding feature to 1
            for trait_name, value in character_traits.items():
                # Only process traits that are in our feature space
                if trait_name in self.trait_to_index:
                    feature_idx = self.trait_to_index[trait_name]
                    # Set to 1 if character has trait (value should be 1 in JSON)
                    X[char_idx, feature_idx] = int(value) if value else 0
        
        # Create labels array (character names)
        y = np.array(character_list)
        
        print(f"[OK] Feature matrix built:")
        print(f"   Shape: {X.shape} ({n_characters} characters × {n_features} features)")
        print(f"   Sparsity: {(1 - X.sum() / (n_characters * n_features)) * 100:.1f}% zeros")
        
        return X, y, character_list
    
    def get_feature_vector(self, character: str) -> np.ndarray:
        """
        Get the feature vector for a single character.
        
        This is useful during gameplay when we need to represent a character
        as a feature vector for prediction or comparison.
        
        Args:
            character: Character name
            
        Returns:
            Feature vector (1D numpy array) with same length as feature_names
            Values are 0 or 1 (binary)
        """
        # Initialize vector with all zeros
        feature_vector = np.zeros(len(self.feature_names), dtype=np.int8)
        
        # If character exists, fill in their traits
        if character in self.traits:
            character_traits = self.traits[character]
            
            # Set features to 1 for traits this character has
            for trait_name, value in character_traits.items():
                if trait_name in self.trait_to_index:
                    feature_idx = self.trait_to_index[trait_name]
                    feature_vector[feature_idx] = int(value) if value else 0
        
        return feature_vector
    
    def get_trait_index(self, trait_name: str) -> int:
        """
        Get the feature index for a given trait name.
        
        This is a helper method for quickly looking up which column
        in the feature vector corresponds to a specific trait.
        
        Args:
            trait_name: Name of the trait (e.g., "abilities_magic")
            
        Returns:
            Feature index (column number) if trait exists, -1 if not found
        """
        return self.trait_to_index.get(trait_name, -1)
    
    def get_question_trait(self, question_idx: int) -> str:
        """
        Get the trait name that a question asks about.
        
        This is useful during gameplay to know which feature
        to update when a user answers a question.
        
        Args:
            question_idx: Index of the question in questions.json
            
        Returns:
            Trait name (e.g., "abilities_magic") or empty string if not found
        """
        return self.question_to_trait.get(question_idx, "")
    
    def create_partial_feature_vector(self, known_traits: Dict[str, int]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create a feature vector with only known traits set.
        
        During gameplay, we only know the answers to questions asked so far.
        This method creates a feature vector with:
        - 1 for traits we know the character HAS
        - 0 for traits we know the character DOESN'T have
        - -1 for traits we DON'T KNOW yet (not asked)
        
        Args:
            known_traits: Dictionary mapping trait_name -> value (0 or 1)
                         Example: {"abilities_magic": 1, "appearance_has_glasses": 0}
        
        Returns:
            feature_vector: Feature vector with -1 for unknown traits
            known_mask: Boolean mask indicating which features are known (True = known, False = unknown)
        """
        # Initialize vector with -1 (unknown) for all features
        feature_vector = np.full(len(self.feature_names), -1, dtype=np.int8)
        
        # Create mask to track which features are known
        known_mask = np.zeros(len(self.feature_names), dtype=bool)
        
        # Fill in known traits
        for trait_name, value in known_traits.items():
            if trait_name in self.trait_to_index:
                feature_idx = self.trait_to_index[trait_name]
                feature_vector[feature_idx] = int(value) if value else 0
                known_mask[feature_idx] = True
        
        return feature_vector, known_mask
    
    def update_feature_vector(self, feature_vector: np.ndarray, question_idx: int, 
                             answer: str, known_mask: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Update a feature vector with a new answer to a question.
        
        During gameplay, when a user answers a question, we need to update
        our feature vector to reflect that new information.
        
        Args:
            feature_vector: Current feature vector (will be modified in place)
            question_idx: Index of the question that was answered
            answer: Answer type: "yes", "no", "probably", "probably_not", "dont_know"
            known_mask: Optional mask tracking which features are known
                       (will be updated if provided)
        
        Returns:
            Updated feature_vector and known_mask (same objects, modified in place)
        """
        # Handle "don't know" - don't update anything
        if answer == "dont_know":
            return feature_vector, known_mask
        
        # Get the trait this question asks about
        trait_name = self.get_question_trait(question_idx)
        
        if not trait_name:
            # Question doesn't map to a trait, nothing to update
            return feature_vector, known_mask
        
        # Get the feature index for this trait
        feature_idx = self.get_trait_index(trait_name)
        
        if feature_idx == -1:
            # Trait not in feature space, nothing to update
            return feature_vector, known_mask
        
        # Map answer to binary value
        # "yes" and "probably" → 1 (has trait)
        # "no" and "probably_not" → 0 (doesn't have trait)
        if answer in ["yes", "probably"]:
            feature_vector[feature_idx] = 1
        elif answer in ["no", "probably_not"]:
            feature_vector[feature_idx] = 0
        else:
            # Unknown answer type - don't update
            return feature_vector, known_mask
        
        # Update the known mask if provided
        # Note: "probably" and "probably_not" are still marked as known, but with lower confidence
        # This will be handled in probability updates
        if known_mask is not None:
            known_mask[feature_idx] = True
        
        return feature_vector, known_mask
    
    def _load_json(self, filepath: str) -> dict:
        """Load JSON file."""
        path = Path(filepath)
        if not path.exists():
            # Try relative to project root
            path = Path(__file__).parent.parent / filepath
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
