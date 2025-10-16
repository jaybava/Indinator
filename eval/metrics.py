def top1_accuracy(results):  # list of dicts from simulate.py
    return sum(r["correct"] for r in results) / max(len(results), 1)

def mean_questions(results):
    return sum(r["questions"] for r in results) / max(len(results), 1)

# TODO: add AU-turns (area under accuracy-vs-budget); simple trapezoid rule.
