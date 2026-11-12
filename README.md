# ticket-aging-by-priority

Age open tickets against per-priority SLA limits from a CSV: P1 0.5 days, P2 1 day, P3 3 days, P4 7 days — BREACH over the limit, AT RISK at 75% of it, otherwise OK, highest priority first with a breach count per priority.

## How to run

```sh
python3 main.py tickets.csv --as-of 2026-11-09
```

## Example output

```
T-1 [P1]: BREACH (created 2026-11-08, 1 day(s) old, SLA 0.5 day(s))
T-2 [P4]: OK (created 2026-11-08, 1 day(s) old, SLA 7 day(s))
P1: 1 breach(es).
P2: 0 breach(es).
P3: 0 breach(es).
P4: 0 breach(es).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
