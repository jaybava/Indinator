"""
Compare Random vs EIG selection using simulated users.
"""
import random
from indinator.kb_store import KBStore
from indinator.engine import Engine
from indinator.selection import select_next_question
from indinator.config import MAX_QUESTIONS

def select_random(pi, entities, remaining_qids, like_fn):
    return random.choice(remaining_qids)

def run_suite(strategy="eig", n=100):
    kb = KBStore("data/questions.json", "data/entities.json", "data/kb.json")
    results = []
    for i in range(n):
        target = random.choice(kb.all_entities())
        eng = Engine(kb.all_entities(), kb.all_questions(), kb.likelihood)
        for t in range(1, MAX_QUESTIONS + 1):
            rem = [q for q in kb.all_questions() if q not in eng.asked]
            q = select_next_question(eng.pi, eng.entities, rem, kb.likelihood) if (strategy=="eig" and t>1) else (rem[0] if t==1 else select_random(eng.pi, eng.entities, rem, kb.likelihood))
            # oracle noiseless:
            a = "yes" if kb.likelihood(target, q) >= 0.5 else "no"
            eng.update(q, a)
            if eng.should_guess(t): break
        g, conf = eng.guess()
        results.append({"target": target, "guess": g, "correct": g==target, "questions": len(eng.asked), "conf": conf})
    return results

if __name__ == "__main__":
    eig = run_suite("eig", 100)
    rnd = run_suite("random", 100)
    from metrics import top1_accuracy, mean_questions
    print("EIG acc:", top1_accuracy(eig), "mean Q:", mean_questions(eig))
    print("RND acc:", top1_accuracy(rnd), "mean Q:", mean_questions(rnd))
