import numpy as np
from indinator.selection import select_next_question

def like(e,q): return 0.9 if e=="a" else 0.1

def test_returns_one_of_remaining():
    pi = np.array([0.5,0.5])
    q = select_next_question(pi, ["a","b"], ["q1","q2"], like)
    assert q in {"q1","q2"}
