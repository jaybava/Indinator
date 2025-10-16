"""
Checks:
- every entity has entries for all questions
- likelihoods in [0,1]
- missing rate <= 3%
"""
import json, sys

def main():
    q = json.load(open("data/questions.json"))
    e = json.load(open("data/entities.json"))
    k = json.load(open("data/kb.json"))
    qids = {x["id"] for x in q["questions"]}
    eids = [x["id"] for x in e["entities"]]

    miss = 0; total = 0
    for eid in eids:
        row = k["likelihoods"].get(eid, {})
        for qid in qids:
            total += 1
            v = row.get(qid, None)
            if v is None: miss += 1
            else:
                if not (0.0 <= float(v) <= 1.0):
                    print(f"ERROR: {eid}.{qid} out of range: {v}"); sys.exit(1)
    mr = miss / max(total,1)
    print(f"Missing cells: {miss}/{total} = {mr:.3%}")
    if mr > 0.03:
        print("ERROR: Missing rate exceeds 3%")
        sys.exit(1)

if __name__ == "__main__":
    main()
