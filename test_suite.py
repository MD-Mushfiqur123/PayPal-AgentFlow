"""
Automated Test Suite for PayPal-AgentFlow.
Tests PayPal Client, Agent Engine, and FastAPI Endpoints.
"""

import unittest
from paypal_client import PayPalClient
from agent_engine import NegotiatorAgent, RiskAuditAgent, SettlementAgent

class TestPayPalAgentFlow(unittest.TestCase):
    def setUp(self):
        self.paypal = PayPalClient()
        self.negotiator = NegotiatorAgent()
        self.risk_auditor = RiskAuditAgent()
        self.settlement = SettlementAgent(self.paypal)

    def test_paypal_client_fallback_order(self):
        order = self.paypal.create_order(amount=250.0, currency="USD", description="Test Invoice")
        self.assertIsNotNone(order.get("id"))
        self.assertEqual(order.get("status"), "CREATED")
        self.assertEqual(order.get("amount"), 250.0)
        self.assertIn("sandbox.paypal.com", order.get("approval_url"))

    def test_negotiator_natural_language_parsing(self):
        prompt = "Create a $350 contract for AI Architecture Consulting with milestone delivery."
        parsed = self.negotiator.parse_intent(prompt)
        self.assertEqual(parsed["total_amount"], 350.0)
        self.assertEqual(parsed["currency"], "USD")
        self.assertEqual(len(parsed["line_items"]), 2)
        self.assertAlmostEqual(parsed["line_items"][0]["amount"], 210.0)
        self.assertAlmostEqual(parsed["line_items"][1]["amount"], 140.0)

    def test_risk_audit_heuristics(self):
        # Small trusted transaction
        low_risk = self.risk_auditor.evaluate_risk(amount=150.0, client_history_count=5)
        self.assertEqual(low_risk.risk_level, "LOW")
        self.assertTrue(low_risk.authorized_for_instant_payout)
        self.assertGreaterEqual(low_risk.trust_score, 85.0)

        # High value anomaly
        high_risk = self.risk_auditor.evaluate_risk(amount=15000.0, velocity_score=0.9)
        self.assertIn(high_risk.risk_level, ["HIGH", "CRITICAL"])
        self.assertFalse(high_risk.authorized_for_instant_payout)

    def test_full_pipeline_execution(self):
        prompt = "Invoice $500 for Edge AI Model Fine-Tuning"
        result = self.settlement.process_natural_language_request(prompt)
        self.assertIn("contract", result)
        self.assertIn("paypal_order", result)
        self.assertEqual(result["contract"]["total_amount"], 500.0)
        self.assertEqual(result["paypal_order"]["status"], "CREATED")
        self.assertGreater(result["pipeline_latency_ms"], 0)

if __name__ == "__main__":
    unittest.main()
