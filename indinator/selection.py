from __future__ import annotations
import numpy as np
from typing import List, Callable
from .config import ANSWER_SET, ANSWER_TO_LIKELIHOOD

def select_next_question(pi: np.ndarray, entities: List[str], remaining_qids: List[str],
                         like_fn: Callable[[str, str], float]) -> str:
    """
    Expected Information Gain (min expected entropy).
    For each question q:
      For each possible canonical answer a:
        - map a to 'y' (strength toward yes)
        - compute per-entity likelihood L_e(a|q) using interpolation
        - compute posterior and its entropy
      take expectation under predictive P(a|q)
    Choose q with min expected entropy (max EIG).
    """
    best_q, best_e = None, +1e9
    for q in remaining_qids:
        E = 0.0
        # Predictive answer distribution via current belief:
        # Approx: P(a|q) = sum_e pi_e * [y*p_yes + (1-y)*(1-p_yes)]
        # Compute once per answer.
        p_yes = np.array([like_fn(e, q) for e in entities])
        for a in ANSWER_SET:
            y = ANSWER_TO_LIKELIHOOD[a]
            like = y * p_yes + (1 - y) * (1 - p_yes)
            pred = float((pi * like).sum())
            if pred == 0:
                continue
            post = (pi * like) / max((pi * like).sum(), 1e-12)
            H = -np.sum(np.where(post > 0, post * np.log(post + 1e-12), 0.0))
            E += pred * H
        if E < best_e:
            best_e, best_q = E, q
    return best_q
