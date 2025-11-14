"""
Game History Learning System
Tracks gameplay data and learns from past games to improve question selection.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


class GameHistoryLearner:
    """Learns from game history to improve AI performance."""
    
    def __init__(self, history_file: str = "data/game_history.json"):
        """Initialize the learning system."""
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(exist_ok=True)
        
        # Load existing history
        self.games = self._load_history()
        
        # Analytics cache
        self._question_effectiveness = None
        self._character_frequency = None
        
    def _load_history(self) -> List[Dict]:
        """Load game history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load game history: {e}")
                return []
        return []
    
    def _save_history(self):
        """Save game history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.games, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save game history: {e}")
    
    def log_game(self, character: str, questions_asked: List[str], 
                 num_questions: int, guesses_made: List[str], 
                 success: bool, traits_asked: List[str],
                 entropy_reductions: Optional[List[float]] = None):
        """
        Log a completed game.
        
        Args:
            character: The actual character
            questions_asked: List of question texts asked
            num_questions: Number of questions asked
            guesses_made: List of incorrect guesses before correct one
            success: Whether the AI guessed correctly
            traits_asked: List of trait IDs asked
            entropy_reductions: List of entropy reduction for each question
        """
        game_record = {
            'timestamp': datetime.now().isoformat(),
            'character': character,
            'questions_asked': questions_asked,
            'traits_asked': traits_asked,
            'num_questions': num_questions,
            'guesses_made': guesses_made,
            'success': success,
            'efficiency_score': 1.0 / num_questions if success else 0.0,
            'entropy_reductions': entropy_reductions or []
        }
        
        self.games.append(game_record)
        self._save_history()
        
        # Invalidate cache
        self._question_effectiveness = None
        self._character_frequency = None
    
    def get_question_effectiveness(self) -> Dict[str, float]:
        """
        Calculate effectiveness score for each trait/question based on:
        1. Entropy reduction (primary metric)
        2. Success rate in successful games
        3. Position in question sequence (earlier = better discriminator)
        
        Returns:
            Dict mapping trait_id to effectiveness score (0-2)
        """
        if self._question_effectiveness is not None:
            return self._question_effectiveness
        
        # Track entropy reduction and success metrics for each trait
        trait_stats = defaultdict(lambda: {
            'entropy_reductions': [],
            'success_count': 0,
            'total_count': 0,
            'positions': []
        })
        
        for game in self.games:
            traits = game['traits_asked']
            num_q = game['num_questions']
            entropy_reds = game.get('entropy_reductions', [])
            
            for i, trait in enumerate(traits):
                trait_stats[trait]['total_count'] += 1
                
                if game['success']:
                    trait_stats[trait]['success_count'] += 1
                    trait_stats[trait]['positions'].append(i / num_q)  # Normalized position
                
                # Track entropy reduction for this question
                if i < len(entropy_reds) and entropy_reds[i] is not None:
                    trait_stats[trait]['entropy_reductions'].append(entropy_reds[i])
        
        # Calculate effectiveness scores
        effectiveness = {}
        for trait, stats in trait_stats.items():
            if stats['total_count'] == 0:
                effectiveness[trait] = 1.0  # Neutral score
                continue
            
            # Component 1: Average entropy reduction (0-1, normalized)
            # Higher entropy reduction = better question
            if stats['entropy_reductions']:
                avg_entropy_reduction = sum(stats['entropy_reductions']) / len(stats['entropy_reductions'])
                # Normalize: typical good questions reduce 0.5-3.0 bits
                entropy_score = min(1.0, avg_entropy_reduction / 2.0)
            else:
                entropy_score = 0.5  # No data, neutral
            
            # Component 2: Success rate
            success_rate = stats['success_count'] / stats['total_count']
            
            # Component 3: Early position bonus (questions asked early are discriminating)
            if stats['positions']:
                avg_pos = sum(stats['positions']) / len(stats['positions'])
                position_bonus = 1.0 - avg_pos  # 0-1, higher for earlier questions
            else:
                position_bonus = 0.5
            
            # Combined score: weighted average
            # Entropy reduction is most important (50%), then success (30%), then position (20%)
            effectiveness[trait] = (
                0.5 * entropy_score +
                0.3 * success_rate +
                0.2 * position_bonus
            )
            
            # Scale to 0-2 range for stronger boosting
            effectiveness[trait] *= 2.0
        
        self._question_effectiveness = effectiveness
        return effectiveness
    
    def get_character_frequency(self) -> Dict[str, int]:
        """
        Get how often each character has been chosen.
        
        Returns:
            Dict mapping character name to selection count
        """
        if self._character_frequency is not None:
            return self._character_frequency
        
        frequency = defaultdict(int)
        for game in self.games:
            frequency[game['character']] += 1
        
        self._character_frequency = dict(frequency)
        return frequency
    
    def get_adaptive_priors(self, characters: List[str], 
                           base_prior: float = 0.01) -> Dict[str, float]:
        """
        Calculate adaptive priors based on character selection frequency.
        
        Args:
            characters: List of all character names
            base_prior: Base prior probability
            
        Returns:
            Dict mapping character to adjusted prior
        """
        frequency = self.get_character_frequency()
        total_games = len(self.games)
        
        if total_games == 0:
            return {char: base_prior for char in characters}
        
        priors = {}
        for char in characters:
            count = frequency.get(char, 0)
            # Blend observed frequency with base prior (Bayesian update)
            observed_prob = count / total_games if total_games > 0 else 0
            # Use 80% observed + 20% base (smoothing)
            priors[char] = 0.8 * observed_prob + 0.2 * base_prior
        
        # Normalize
        total = sum(priors.values())
        if total > 0:
            priors = {char: prob / total for char, prob in priors.items()}
        
        return priors
    
    def get_question_boost(self, trait: str) -> float:
        """
        Get learned boost factor for a question based on historical effectiveness.
        Uses entropy reduction, success rate, and position data.
        
        Args:
            trait: Trait ID
            
        Returns:
            Boost multiplier (0.3 to 2.5)
        """
        if len(self.games) < 3:
            return 1.0  # Not enough data yet
        
        effectiveness = self.get_question_effectiveness()
        
        if trait in effectiveness:
            score = effectiveness[trait]  # 0-2 range
            # Map 0-2 effectiveness to 0.3-2.5 multiplier
            # Poor questions (0) get 0.3x, average (1) get 1.15x, excellent (2) get 2.5x
            return 0.3 + 1.1 * score
        
        return 1.0  # Neutral for unseen questions
    
    def get_stats(self) -> Dict:
        """Get learning statistics."""
        if len(self.games) == 0:
            return {
                'total_games': 0,
                'success_rate': 0.0,
                'avg_questions': 0.0,
                'most_picked': [],
                'learning_active': False
            }
        
        successful = [g for g in self.games if g['success']]
        frequency = self.get_character_frequency()
        most_picked = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_games': len(self.games),
            'success_rate': len(successful) / len(self.games),
            'avg_questions': sum(g['num_questions'] for g in successful) / len(successful) if successful else 0,
            'most_picked': most_picked,
            'learning_active': len(self.games) >= 5
        }

