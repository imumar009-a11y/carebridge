"""Runs test_cases.csv and prints accuracy. Run: python run_tests.py"""
import csv, time
from core import triage, LEVELS

rows = list(csv.DictReader(open("test_cases.csv", encoding="utf-8")))
exact = under = 0
for r in rows:
    got = triage(r["message"], log=False)["urgency"]
    exp = r["expected"]
    ok = got == exp
    # under-triage = app was LESS urgent than expected (the dangerous mistake)
    risky = got not in LEVELS or LEVELS.index(got) < LEVELS.index(exp)
    exact += ok
    under += risky
    r["got"], r["result"] = got, "PASS" if ok else ("UNDER-TRIAGE" if risky else "over-cautious")
    print(r["result"], "|", r["message"], "|", exp, "->", got)
    time.sleep(1)
n = len(rows)
print(f"\nExact accuracy: {exact}/{n} = {100*exact/n:.0f}%")
print(f"Under-triage (dangerous): {under}/{n}")
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)