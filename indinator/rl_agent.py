"""
Reinforcement Learning Agent for Question Selection
Uses Q-Learning to learn optimal question selection policy.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class RLQuestionAgent:
    """
    Q-Learning agent that learns optimal question selection policy.
    
    State: (entropy_bucket, top_prob_bucket, questions_asked, remaining_candidates)
    Action: Question/trait ID
    Reward: -1 per question, +100 for correct guess, -50 for wrong guess
    """
    
    def __init__(self, q_table_file: str = "data/q_table.json", 
                 alpha: float = 0.15, gamma: float = 0.97, epsilon: float = 0.25):
        """
        Initialize RL agent.
        
        Args:
            q_table_file: Path to save/load Q-table
            alpha: Learning rate (0-1)
            gamma: Discount factor (0-1)
            epsilon: Exploration rate (0-1)
        """
        self.q_table_file = Path(q_table_file)
        self.q_table_file.parent.mkdir(exist_ok=True)
        
        # Hyperparameters
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = 0.992  # Decay epsilon over time
        self.epsilon_min = 0.05  # Minimum exploration
        
        # Q-table: Q[state][action] = expected value
        self.q_table = self._load_q_table()
        
        # Episode tracking
        self.current_episode = []  # [(state, action, reward), ...]
        self.episode_count = 0
        
    def _load_q_table(self) -> Dict:
        """Load Q-table from file."""
        if self.q_table_file.exists():
            try:
                with open(self.q_table_file, 'r') as f:
                    data = json.load(f)
                    self.episode_count = data.get('episode_count', 0)
                    return defaultdict(lambda: defaultdict(float), data.get('q_values', {}))
            except Exception as e:
                print(f"Warning: Could not load Q-table: {e}")
        return defaultdict(lambda: defaultdict(float))
    
    def _save_q_table(self):
        """Save Q-table to file."""
        try:
            # Convert defaultdicts to regular dicts for JSON
            q_values = {
                state: dict(actions) 
                for state, actions in self.q_table.items()
            }
            
            data = {
                'q_values': q_values,
                'episode_count': self.episode_count,
                'alpha': self.alpha,
                'gamma': self.gamma,
                'epsilon': self.epsilon
            }
            
            with open(self.q_table_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save Q-table: {e}")
    
    def get_state(self, entropy: float, top_prob: float, 
                  questions_asked: int, remaining_candidates: int) -> str:
        """
        Convert continuous game state to discrete state representation.
        
        Args:
            entropy: Current entropy of probability distribution
            top_prob: Probability of top character
            questions_asked: Number of questions asked so far
            remaining_candidates: Number of viable candidates
            
        Returns:
            State string for Q-table lookup
        """
        # Discretize continuous values into buckets
        entropy_bucket = min(4, int(entropy))  # 0-4
        top_prob_bucket = int(top_prob * 10)  # 0-10 (0.0-1.0 -> 0-10)
        questions_bucket = min(5, questions_asked // 5)  # 0-5 (groups of 5)
        candidates_bucket = min(5, remaining_candidates // 10)  # 0-5 (groups of 10)
        
        return f"{entropy_bucket}_{top_prob_bucket}_{questions_bucket}_{candidates_bucket}"
    
    def select_action(self, state: str, available_actions: List[str], 
                     use_epsilon_greedy: bool = True) -> str:
        """
        Select action using epsilon-greedy policy.
        
        Args:
            state: Current state
            available_actions: List of valid trait IDs to ask about
            use_epsilon_greedy: Whether to use exploration (True) or pure exploitation (False)
            
        Returns:
            Selected trait ID
        """
        if not available_actions:
            return None
        
        # Epsilon-greedy exploration
        if use_epsilon_greedy and np.random.random() < self.epsilon:
            # Explore: random action
            return np.random.choice(available_actions)
        
        # Exploit: choose best known action
        q_values = self.q_table[state]
        
        # Get Q-values for available actions
        action_q_values = [(action, q_values.get(action, 0.0)) for action in available_actions]
        
        if not action_q_values:
            return np.random.choice(available_actions)
        
        # Choose action with highest Q-value
        best_action = max(action_q_values, key=lambda x: x[1])[0]
        return best_action
    
    def get_action_value(self, state: str, action: str) -> float:
        """
        Get Q-value for state-action pair.
        
        Args:
            state: State string
            action: Trait ID
            
        Returns:
            Q-value (expected future reward)
        """
        return self.q_table[state].get(action, 0.0)
    
    def record_step(self, state: str, action: str, reward: float):
        """
        Record a step in the current episode.
        
        Args:
            state: State before action
            action: Action taken (trait ID)
            reward: Immediate reward received
        """
        self.current_episode.append((state, action, reward))
    
    def update_q_value(self, state: str, action: str, reward: float, next_state: str):
        """
        Update Q-value using Q-learning update rule.
        
        Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)]
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state reached
        """
        # Get current Q-value (default to 0.0 for new state-action pairs)
        current_q = self.q_table[state].get(action, 0.0)
        
        # Get max Q-value for next state
        max_next_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0.0
        
        # Q-learning update
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        
        self.q_table[state][action] = new_q
    
    def end_episode(self, success: bool, total_questions: int):
        """
        Complete the episode and update Q-values.
        
        Args:
            success: Whether the AI guessed correctly
            total_questions: Total number of questions asked
        """
        if not self.current_episode:
            return
        
        # Calculate terminal reward
        if success:
            # Reward inversely proportional to questions asked
            # Perfect game (5 questions) = +50, average (15) = +20, slow (25) = +5
            terminal_reward = max(5.0, 100.0 / total_questions)
        else:
            # Penalty for failure
            terminal_reward = -50.0
        
        # Backward pass through episode with discounted rewards
        cumulative_reward = terminal_reward
        
        # Update Q-values from end to start (backward)
        for i in range(len(self.current_episode) - 1, -1, -1):
            state, action, step_reward = self.current_episode[i]
            
            # Each question costs -1
            total_reward = step_reward + cumulative_reward
            
            # Get next state (or terminal)
            if i < len(self.current_episode) - 1:
                next_state = self.current_episode[i + 1][0]
            else:
                next_state = "terminal"
            
            # Update Q-value
            self.update_q_value(state, action, total_reward, next_state)
            
            # Discount for previous steps
            cumulative_reward = self.gamma * cumulative_reward
        
        # Decay epsilon (reduce exploration over time)
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        # Increment episode count
        self.episode_count += 1
        
        # Clear episode
        self.current_episode = []
        
        # Save periodically
        if self.episode_count % 5 == 0:
            self._save_q_table()
    
    def get_stats(self) -> Dict:
        """Get RL agent statistics."""
        return {
            'episode_count': self.episode_count,
            'epsilon': self.epsilon,
            'q_table_size': sum(len(actions) for actions in self.q_table.values()),
            'unique_states': len(self.q_table),
            'learning_active': self.episode_count >= 5
        }

