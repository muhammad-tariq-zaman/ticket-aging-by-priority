import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import age_tickets

import datetime
AS_OF = datetime.date(2026, 11, 9)

def row(ticket, priority, created):
    return {"ticket": ticket, "priority": priority, "created": created}

class TestTicketAgingByPriority(unittest.TestCase):
    def test_p1_one_day_is_breach(self):
        self.assertEqual(age_tickets([row("T-1", "P1", "2026-11-08")], AS_OF)[0][5], "BREACH")
    def test_p1_same_day_is_ok(self):
        self.assertEqual(age_tickets([row("T-1", "P1", "2026-11-09")], AS_OF)[0][5], "OK")
    def test_p4_one_day_is_ok(self):
        self.assertEqual(age_tickets([row("T-1", "P4", "2026-11-08")], AS_OF)[0][5], "OK")
    def test_p3_three_days_is_at_risk(self):
        self.assertEqual(age_tickets([row("T-1", "P3", "2026-11-06")], AS_OF)[0][5], "AT RISK")
    def test_p2_two_days_is_breach(self):
        self.assertEqual(age_tickets([row("T-1", "P2", "2026-11-07")], AS_OF)[0][5], "BREACH")
    def test_unknown_priority_uses_p4_limit(self):
        self.assertEqual(age_tickets([row("T-1", "P9", "2026-11-08")], AS_OF)[0][4], 7.0)
    def test_age_computed(self):
        self.assertEqual(age_tickets([row("T-1", "P4", "2026-11-01")], AS_OF)[0][3], 8)
    def test_highest_priority_first(self):
        r = age_tickets([row("T-9", "P4", "2026-11-01"), row("T-1", "P1", "2026-11-08")], AS_OF)
        self.assertEqual(r[0][0], "T-1")
