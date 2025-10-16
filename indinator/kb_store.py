from __future__ import annotations
import json
from typing import Dict, List

class KBStore:
    """Loads questions, entities, and likelihood matrix. Provides safe accessors."""
    def __init__(self, questions_path: str, entities_path: str, kb_path: str):
        self.questions = self._load(questions_path)["questions"]
        self.entities = self._load(entities_path)["entities"]
        self.kb = self._load(kb_path)["likelihoods"]
        self._index()

    def _index(self):
        self.entity_ids = [e["id"] for e in self.entities]
        self.question_ids = [q["id"] for q in self.questions]

    def _load(self, p: str):
        with open(p, "r") as f: return json.load(f)

    def likelihood(self, entity_id: str, question_id: str) -> float:
        # TODO: add smoothing if missing; for now assume validated kb
        return float(self.kb[entity_id][question_id])

    def all_entities(self) -> List[str]: return self.entity_ids
    def all_questions(self) -> List[str]: return self.question_ids
