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


# --- input validation regressions ---------------------------------------------

@pytest.mark.parametrize("email,expected", [
    ("a@@uni.edu", "REJECTED"),   # two '@'
    ("a@.edu", "REJECTED"),       # no real domain
    ("me.edu", "REJECTED"),       # no '@' at all
])
def test_registration_email_rules(email, expected):
    r = run("Smart Registration System.py", f"CSE-123\n{email}\nSecret123\nREF12x@\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().endswith(expected)


@pytest.mark.parametrize("email,age", [
    ("a.b@c", "25"),        # no dot in the domain
    ("a@@x.com", "25"),     # two '@'
    ("jane@x.com", "abc"),  # non-numeric age used to crash
])
def test_profile_invalid_inputs(email, age):
    r = run("User Profile Validation System.py", f"Jane Doe\n{email}\n9876543210\n{age}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().endswith("User Profile is INVALID")


def test_performance_non_numeric_mark_is_invalid():
    r = run("Student Performance Analyzer.py", "Aniket\n2\n95\nabc\n")
    assert r.returncode == 0, r.stderr
    assert "abc -> Invalid" in r.stdout
    assert "Total Invalid Students: 1" in r.stdout


def test_performance_negative_count_exits_cleanly():
    r = run("Student Performance Analyzer.py", "Aniket\n-2\n")
    assert "at least 1" in r.stderr and "Traceback" not in r.stderr


def test_list_filter_empty_list_after_personalization():
    r = run("Smart List Filter & Rebuilder.py", "Aniket\n3\na\nb\nc\n")
    assert r.returncode == 0, r.stderr
    after = r.stdout.split("After Personalization:")[1]
    assert "Numbers List: []" in after   # used to print ['', '']


def test_list_filter_whitespace_entry_is_skipped():
    r = run("Smart List Filter & Rebuilder.py", "Aniket\n2\n   \nb\n")
    assert "Total Strings: 1" in r.stdout


@pytest.mark.parametrize("script,stdin", [
    ("Smart Transport Load Balancing System.py", "2\n5\nx\n"),
    ("Smart Transport Load Balancing System.py", "0\n"),
    ("Smart Campus Energy Analyzer.py", "2\n10\nabc\n"),
    ("Smart Playlist Intelligence System.py", "two\n"),
])
def test_bad_numeric_input_exits_without_traceback(script, stdin):
    r = run(script, stdin)
    assert r.returncode != 0
    assert "Traceback" not in r.stderr and r.stderr.strip()


def test_playlist_non_numeric_duration_is_invalid():
    r = run("Smart Playlist Intelligence System.py", "2\n100\n3:20\n")
    assert r.returncode == 0, r.stderr
    assert "Invalid Song duration" in r.stdout


def test_replication_reports_secure_count():
    r = run("Multi-Level Data Replication & Integrity Analyzer.py", "")
    assert r.returncode == 0, r.stderr
    assert "tuple -> (2, 0," in r.stdout   # both records leaked, none secure
