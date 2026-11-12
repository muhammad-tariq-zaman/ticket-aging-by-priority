"""Age open tickets against per-priority SLA limits.

Usage: python3 main.py tickets.csv [--as-of 2026-11-09]
CSV columns: ticket,priority,created (ISO date).
SLA limits in days: P1 0.5, P2 1, P3 3, P4 7.
Age = reference date minus created date, in whole days.
- BREACH: age is over the SLA limit.
- AT RISK: age is at least 75% of the SLA limit.
- OK: younger than 75% of the SLA limit.
Highest priority first, oldest first within it, plus a breach
count per priority at the end.
"""
import argparse, csv, sys
from datetime import date

SLA_DAYS = {"P1": 0.5, "P2": 1.0, "P3": 3.0, "P4": 7.0}

def age_tickets(rows, as_of=None):
    as_of = as_of or date.today()
    out = []
    for row in rows:
        priority = row["priority"].strip().upper()
        created = date.fromisoformat(row["created"].strip())
        age = (as_of - created).days
        limit = SLA_DAYS.get(priority, 7.0)
        if age > limit:
            verdict = "BREACH"
        elif age >= limit * 0.75:
            verdict = "AT RISK"
        else:
            verdict = "OK"
        out.append((row["ticket"].strip(), priority, created.isoformat(),
                    age, limit, verdict))
    return sorted(out, key=lambda r: (r[1], -r[3]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--as-of", default=None, help="reference date YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    with open(args.path, newline="", encoding="utf-8") as f:
        results = age_tickets(list(csv.DictReader(f)), as_of)
    for ticket, priority, created, age, limit, verdict in results:
        print(f"{ticket} [{priority}]: {verdict} (created {created}, {age} day(s) old, SLA {limit:g} day(s))")
    for priority in ("P1", "P2", "P3", "P4"):
        breaches = sum(1 for r in results if r[1] == priority and r[5] == "BREACH")
        print(f"{priority}: {breaches} breach(es).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
