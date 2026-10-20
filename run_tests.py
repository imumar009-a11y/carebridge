"""Runs test_cases.csv and prints accuracy.

    python run_tests.py            # uses Gemini if GEMINI_API_KEY is set, otherwise rules only
    python run_tests.py --offline  # rules only (no network, no key)

These are REGRESSION tests written by the developer, not clinical validation.
"""
import csv
import sys
import time
from cb import ai
from cb.config import LEVELS
from cb.triage import triage

offline = "--offline" in sys.argv or not ai.available()
print("Mode:", "rules only (offline)" if offline else "rules + Gemini")
with open("test_cases.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
exact = under = 0
for r in rows:
    got = triage(r["message"], log=False, use_ai=not offline)["urgency"]
    exp = r["expected"]
    ok = got == exp
    # under-triage = app was LESS urgent than expected (the dangerous mistake)
    risky = got not in LEVELS or LEVELS.index(got) < LEVELS.index(exp)
    exact += ok
    under += risky
    r["got"], r["result"] = got, "PASS" if ok else ("UNDER-TRIAGE" if risky else "over-cautious")
    if not ok or "--verbose" in sys.argv:
        print(r["result"], "|", r["message"], "|", exp, "->", got)
    if not offline:
        time.sleep(1)
n = len(rows)
print("\nExact accuracy: %d/%d = %.0f%%" % (exact, n, 100 * exact / n))
print("Under-triage (dangerous): %d/%d" % (under, n))
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
