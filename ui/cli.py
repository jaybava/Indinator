from indinator.kb_store import KBStore
from indinator.engine import Engine
from indinator.selection import select_next_question
from indinator.config import MAX_QUESTIONS

QUESTIONS = "data/questions.json"
ENTITIES  = "data/entities.json"
KB        = "data/kb.json"

def main():
    kb = KBStore(QUESTIONS, ENTITIES, KB)
    eng = Engine(kb.all_entities(), kb.all_questions(), kb.likelihood)

    asked = set()
    for t in range(1, MAX_QUESTIONS + 1):
        remaining = [q for q in kb.all_questions() if q not in asked]
        q = remaining[0] if t == 1 else select_next_question(eng.pi, eng.entities, remaining, kb.likelihood)
        asked.add(q)
        # Sprint 0 behavior: no logic required; but we’ll collect an answer anyway:
        ans = input(f"Q{t}: {q} (yes/no/probably/probably_not/unknown) > ").strip().lower()
        eng.update(q, ans)
        if eng.should_guess(t):
            guess, conf = eng.guess()
            print(f"\nI guess: {guess} (confidence={conf:.2f})")
            break

if __name__ == "__main__":
    main()
