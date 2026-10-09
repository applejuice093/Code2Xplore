"""Smoke tests: run each interactive script with scripted stdin and check the output."""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def run(script, stdin):
    return subprocess.run([sys.executable, str(ROOT / script)], input=stdin,
                          capture_output=True, text=True, timeout=60)


@pytest.mark.parametrize("stdin,expected", [
    ("CSE-123\nme@uni.edu\nSecret123\nREF12x@\n", "APPROVED"),
    ("CSE-123\nme@uni.edu\nsecret123\nREF12x@\n", "REJECTED"),  # lowercase first letter
    ("CS\nme@uni.edu\nSecret123\nREF12x@\n", "REJECTED"),       # short ID, used to crash
    ("CSE-123\nme@uni.edu\nSecret123\nRE\n", "REJECTED"),        # short referral, used to crash
])
def test_registration(stdin, expected):
    r = run("Smart Registration System.py", stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().endswith(expected)


@pytest.mark.parametrize("stdin,expected", [
    ("Jane Doe\njane@x.com\n9876543210\n25\n", "VALID"),
    ("\njane@x.com\n9876543210\n25\n", "INVALID"),
])
def test_profile(stdin, expected):
    r = run("User Profile Validation System.py", stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().endswith(f"User Profile is {expected}")


def test_performance():
    r = run("Student Performance Analyzer.py", "Aniket\n3\n95\n30\n150\n")
    assert r.returncode == 0, r.stderr
    assert "Total Failed Students: 1" in r.stdout
    assert "Total Invalid Students: 1" in r.stdout


def test_list_filter_negative_numbers():
    r = run("Smart List Filter & Rebuilder.py", "Aniket\n3\n-5\nabc\n7\n")
    assert r.returncode == 0, r.stderr
    assert "Numbers List: [-5, 7]" in r.stdout


def test_energy_zero_buildings_exits_cleanly():
    r = run("Smart Campus Energy Analyzer.py", "0\n")
    assert "at least 1" in r.stderr and "Traceback" not in r.stderr


def test_playlist():
    r = run("Smart Playlist Intelligence System.py", "2\n100\n100\n")
    assert "Repetitive Playlist" in r.stdout


def test_transport():
    r = run("Smart Transport Load Balancing System.py", "3\n2\n30\n70\n")
    assert r.returncode == 0, r.stderr
    assert "Number of PLI affected Items:" in r.stdout


def test_replication_analyzer():
    r = run("Multi-Level Data Replication & Integrity Analyzer.py", "")
    assert r.returncode == 0, r.stderr


def test_city_analyzer():
    pytest.importorskip("pandas")
    r = run("City Analyzer.py", "")
    assert r.returncode == 0, r.stderr
    assert "System Decision:" in r.stdout
