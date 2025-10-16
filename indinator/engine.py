from __future__ import annotations
from typing import Dict, List, Tuple
import numpy as np
from .config import ANSWER_TO_LIKELIHOOD, STOP_CONFIDENCE, MAX_QUESTIONS

class Engine:
    """
    Maintains belief π over entities; updates with Bayes rule given (q, a).
    """
    def __init__(self, entities: List[str], question_ids: List[str], like_fn):
        self.entities = entities
        self.questions = question_ids
        self.like_fn = like_fn  # (entity_id, question_id) -> p(answer="yes"|entity)
        self.reset()

    def reset(self):
        self.pi = np.ones(len(self.entities)) / len(self.entities)
        self.asked = []
        self.log = []

    def map_answer_to_likelihood(self, ans: str) -> float:
        return ANSWER_TO_LIKELIHOOD.get(ans, 0.5)

    def update(self, q_id: str, ans: str):
        y = self.map_answer_to_likelihood(ans)
        # Likelihood for all entities given the question:
        L = np.array([self._interp_likelihood(e, q_id, y) for e in self.entities])
        self.pi = L * self.pi
        s = self.pi.sum()
        if s == 0:  # fallback if all zero due to extreme inputs
            self.pi = np.ones_like(self.pi) / len(self.pi)
        else:
            self.pi /= s
        self.asked.append(q_id)
        self.log.append({"q": q_id, "ans": ans, "top": self.top_k(5)})

    def _interp_likelihood(self, e_id: str, q_id: str, y: float) -> float:
        """
        We store p_yes := P(answer=yes | entity). For other answers, linearly interpolate:
        - yes       -> y (≈ 0.95)
        - no        -> 1 - y (≈ 0.05)
        - probably  -> mix(0.5,y)
        - probably_not -> mix(0.5,1-y)
        - unknown   -> 0.5
        For simplicity: weight = y if ans maps to y; else (1-y) etc. Caller passes y already.
        But we need p_yes to derive consistency: use convex combo around p_yes.
        """
        p_yes = float(self.like_fn(e_id, q_id))  # from kb
        # Interpret 'y' as "strength toward yes". Blend toward yes/no:
        return y * p_yes + (1 - y) * (1 - p_yes)

    def should_guess(self, t: int) -> bool:
        return (self.pi.max() >= STOP_CONFIDENCE) or (t >= MAX_QUESTIONS)

    def guess(self) -> Tuple[str, float]:
        idx = int(self.pi.argmax())
        return self.entities[idx], float(self.pi[idx])

    def top_k(self, k: int) -> List[Tuple[str, float]]:
        idxs = np.argsort(-self.pi)[:k]
        return [(self.entities[i], float(self.pi[i])) for i in idxs]
