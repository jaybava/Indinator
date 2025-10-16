"""
Reports coverage per question and basic sparsity stats.
"""
import json
from collections import defaultdict

q = json.load(open("data/questions.json"))
e = json.load(open("data/entities.json"))
k = json.load(open("data/kb.json"))

qids = [x["id"] for x in q["questions"]]
eids = [x["id"] for x in e["entities"]]

counts = defaultdict(int)
for qid in qids:
    for eid in eids:
        if qid in k["likelihoods"].get(eid, {}): counts[qid] += 1

for qid in qids:
    cov = counts[qid] / max(len(eids),1)
    print(f"{qid}: coverage={cov:.1%}")
