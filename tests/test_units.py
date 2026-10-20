"""Unit tests for the scripts that expose importable functions (Day 8 and Day 9)."""
import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load(filename, name):
    """Import a script whose file name contains spaces or '&'."""
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- Day 9: Multi-Level Data Replication & Integrity Analyzer -----------------

@pytest.fixture(scope="module")
def rep():
    return load("Multi-Level Data Replication & Integrity Analyzer.py", "replication")


def test_replicate_data_identity(rep):
    root = rep.generate_data()
    alias, shallow, deep = rep.replicate_data(root)
    assert alias is root
    assert shallow is not root and shallow[0] is root[0]      # shares inner dicts
    assert deep == root and deep[0] is not root[0]            # shares nothing


def test_integrity_untouched_data_is_all_secure(rep):
    root = rep.generate_data()
    snapshot = copy.deepcopy(root)
    leaks, secure, overlap = rep.check_integrity(snapshot, root, copy.copy(root))
    assert (leaks, secure) == (0, 2)
    assert overlap == 4  # a/b/c/d.txt all shared with the shallow copy


def test_integrity_counts_leaks_and_secure_separately(rep):
    root = rep.generate_data()
    snapshot = copy.deepcopy(root)
    alias, shallow, deep = rep.replicate_data(root)
    rep.modify_data(root, alias, shallow, deep, "dev", 11701)
    leaks, secure, _ = rep.check_integrity(snapshot, root, shallow)
    assert leaks == 2           # alias id change + shallow file/usage changes
    assert leaks + secure == len(snapshot)
    assert deep[0]["data"]["usage"] == 0 and root[0]["data"]["usage"] == 500


@pytest.mark.parametrize("roll,files", [(11701, ["a.txt"]), (11702, ["a.txt", "b.txt", "newfile_11702.txt"])])
def test_modify_data_odd_even_roll(rep, roll, files):
    root = rep.generate_data()
    alias, shallow, deep = rep.replicate_data(root)
    rep.modify_data(root, alias, shallow, deep, "dev", roll)
    assert root[0]["data"]["files"] == files      # shallow change leaks into root
    assert len(root) == 2 and len(shallow) == 3   # appended record does not


# --- Day 8: City Analyzer -----------------------------------------------------

@pytest.fixture(scope="module")
def city():
    pytest.importorskip("pandas")
    return load("City Analyzer.py", "city_analyzer")


def zone(z, t, a, e):
    return {"zone": z, "traffic": t, "air_quality": a, "energy": e}


def test_generate_city_data_ranges(city):
    data = city.generate_city_data(20)
    assert [d["zone"] for d in data] == list(range(1, 21))
    for d in data:
        assert 0 <= d["traffic"] <= 100
        assert 0 <= d["air_quality"] <= 300
        assert 0 <= d["energy"] <= 500


def test_generate_city_data_rejects_zero_zones(city):
    with pytest.raises(ValueError):
        city.generate_city_data(0)


def test_classify_zones(city):
    data = [
        zone(1, 90, 50, 100),    # high traffic -> High Risk
        zone(2, 50, 250, 450),   # bad AQI + high energy -> High Risk and Energy Critical
        zone(3, 50, 150, 450),   # energy only -> Energy Critical
        zone(4, 10, 50, 100),    # calm -> Safe Zone
        zone(5, 50, 150, 100),   # nothing -> Unclassified
    ]
    cats = city.classify_zones(data)
    assert cats["High Risk"] == {1, 2}
    assert cats["Energy Critical"] == {2, 3}
    assert cats["Safe Zone"] == {4}
    assert cats["Unclassified"] == {5}


def test_personalized_rule_sorts_by_traffic(city, capsys):
    data = [zone(1, 70, 0, 0), zone(2, 10, 0, 0), zone(3, 40, 0, 0)]
    result = city.apply_personalized_rule(data, 11620)  # not divisible by 3
    assert [d["traffic"] for d in result] == [10, 40, 70]
    assert "bubble sort" in capsys.readouterr().out


def test_personalized_rule_shuffle_keeps_items(city):
    data = [zone(i, i * 5, 0, 0) for i in range(1, 8)]
    result = city.apply_personalized_rule(list(data), 9)  # divisible by 3
    assert sorted(d["zone"] for d in result) == list(range(1, 8))


def test_decision_city_stable(city):
    import pandas as pd
    df = pd.DataFrame([zone(i, 10, 10, 10) for i in range(1, 4)])  # risk_score ~3.16
    assert city.analyze_and_detect_patterns(df) == "City Stable"


def test_decision_critical_emergency(city):
    import pandas as pd
    df = pd.DataFrame([zone(i, 100, 300, 500) for i in range(1, 4)])  # risk_score ~17.3
    assert city.analyze_and_detect_patterns(df) == "Critical Emergency"


def test_decision_high_alert_from_cluster(city, capsys):
    import pandas as pd
    df = pd.DataFrame([zone(1, 85, 10, 0), zone(2, 85, 10, 0), zone(3, 0, 0, 0)])
    assert city.analyze_and_detect_patterns(df) == "High Alert"
    out = capsys.readouterr().out
    assert "(1, 2)" in out
    assert "np." not in out  # no np.float64(...)/np.int64(...) reprs in the report
