import numpy as np
from indinator.engine import Engine

def like(e,q):
    table = {("a","q1"):0.9, ("b","q1"):0.1}
    return table[(e,q)]

def test_update_normalizes():
    eng = Engine(["a","b"], ["q1"], like)
    eng.update("q1","yes")
    assert np.isclose(eng.pi.sum(), 1.0)

def test_guess_ordering():
    eng = Engine(["a","b"], ["q1"], like)
    eng.update("q1","yes")
    g, p = eng.guess()
    assert g == "a"
    assert p > 0.5
