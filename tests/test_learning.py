from indinator.learning import BetaStore

def test_beta_mean(tmp_path):
    p = tmp_path/"beta.json"
    p.write_text('{"version":1,"beta":{"e":{"q":{"alpha":2,"beta":2}}}}')
    b = BetaStore(str(p))
    assert abs(b.mean("e","q") - 0.5) < 1e-6
