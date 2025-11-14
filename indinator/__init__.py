"""
Indinator - AI-based Akinator Clone
An intelligent character guessing game using Bayesian inference, entropy-based question selection,
and machine learning from game history.
"""

from .ai_engine import AkinatorAI
from .game import AkinatorGame
from .game_history import GameHistoryLearner
from .rl_agent import RLQuestionAgent

__version__ = "2.5.0"  # RL-enhanced version
__all__ = ['AkinatorAI', 'AkinatorGame', 'GameHistoryLearner', 'RLQuestionAgent']

