from __future__ import annotations
import json
from typing import Dict

class BetaStore:
    def __init__(self, path: str):
        self.path = path
        with open(path, "r") as f:
            data = json.load(f)
        self.beta = data["beta"]

    def mean(self, e_id: str, q_id: str) -> float:
        a, b = self.beta[e_id][q_id]["alpha"], self.beta[e_id][q_id]["beta"]
        return a / (a + b)

    def update(self, e_id: str, q_id: str, ans_strength: float, weight: float = 1.0):
        """
        ans_strength in [0,1], where 1→yes, 0→no, 0.5→unknown.
        Fractional updates: alpha += weight*ans_strength; beta += weight*(1-ans_strength)
        """
        b = self.beta[e_id][q_id]
        b["alpha"] += weight * ans_strength
        b["beta"]  += weight * (1 - ans_strength)

    def persist(self):
        with open(self.path, "w") as f:
            json.dump({"version": 1, "beta": self.beta}, f, indent=2)

def update_beta_from_game(beta_store: BetaStore, correct_entity: str, game_log):
    """
    game_log: [{q, ans, top}, ...]
    Map answers onto strengths: yes=1, no=0, probably=0.75, probably_not=0.25, unknown=0.5
    """
    map_strength = {"yes":1.0,"no":0.0,"probably":0.75,"probably_not":0.25,"unknown":0.5}
    for step in game_log:
        q, a = step["q"], step["ans"]
        s = map_strength.get(a, 0.5)
        beta_store.update(correct_entity, q, s, weight=1.0)
