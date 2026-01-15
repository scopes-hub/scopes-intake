import unittest
from pathlib import Path

from app import scoring


class ScoreLeadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[1]
        scoring.RULES_PATH = str(root / "config" / "scoring_rules.json")
        cls.rules = scoring.load_rules(force_reload=True)

    def test_partnerships_route(self) -> None:
        payload = {
            "industry": "Software",
            "company_size": "Enterprise",
            "region": "NA",
            "email": "jamie@acme.com",
        }
        score, route = scoring.score_lead(payload, self.rules)
        self.assertEqual(score, 95)
        self.assertEqual(route, "Partnerships")

    def test_sales_route(self) -> None:
        payload = {
            "industry": "Finance",
            "company_size": "Mid-Market",
            "region": "EMEA",
            "email": "rene@northwind.com",
        }
        score, route = scoring.score_lead(payload, self.rules)
        self.assertEqual(score, 70)
        self.assertEqual(route, "Sales")

    def test_support_route(self) -> None:
        payload = {
            "industry": "Education",
            "company_size": "SMB",
            "region": "LATAM",
            "email": "someone@gmail.com",
        }
        score, route = scoring.score_lead(payload, self.rules)
        self.assertEqual(score, 18)
        self.assertEqual(route, "Support")
