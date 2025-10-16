"""
Simulated user answers from KB with optional 10% noise.
"""
import random
from indinator.kb_store import KBStore
from indinator.engine import Engine
from indinator.selection import select_next_question
from indinator.config import MAX_QUESTIONS

def noisy_answer(p_yes: float, noise=0.1):
    # sample ground truth yes/no from p_yes, then flip with prob=noise; map to canonical answer
    y = random.random() < p_yes
    if random.random() < noise: y = not y
    return "yes" if y else "no"

def run_one_game(kb: KBStore, target_id: str, noise=0.1):
    eng = Engine(kb.all_entities(), kb.all_questions(), kb.likelihood)
    for t in range(1, MAX_QUESTIONS + 1):
        remaining = [q for q in kb.all_questions() if q not in eng.asked]
        q = select_next_question(eng.pi, eng.entities, remaining, kb.likelihood) if t > 1 else remaining[0]
        # oracle answer from KB for the target:
        p_yes = kb.likelihood(target_id, q)
        a = noisy_answer(p_yes, noise=noise)
        eng.update(q, a)
        if eng.should_guess(t):
            g, conf = eng.guess()
            return {"target": target_id, "guess": g, "correct": g == target_id, "questions": t, "conf": conf}
    g, conf = eng.guess()
    return {"target": target_id, "guess": g, "correct": g == target_id, "questions": MAX_QUESTIONS, "conf": conf}

if __name__ == "__main__":
    kb = KBStore("data/questions.json", "data/entities.json", "data/kb.json")
    stats = [run_one_game(kb, e) for e in kb.all_entities()[:50]]
    acc = sum(s["correct"] for s in stats) / len(stats)
    print(f"Simulated ACC: {acc:.3f}")
