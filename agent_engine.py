"""
Multi-Agent Commerce & Fraud Risk Engine for PayPal-AgentFlow.
Coordinates Negotiator, Risk Audit, and Settlement Agents.
Architect: Mushfiqur Rahim & L
"""

import re
import time
import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class LineItem:
    description: str
    amount: float
    milestone_id: str
    verified: bool = False

@dataclass
class RiskEvaluation:
    trust_score: float # 0 - 100
    risk_level: str # LOW, MEDIUM, HIGH, CRITICAL
    anomaly_flags: List[str]
    max_recommended_hold_hours: int
    authorized_for_instant_payout: bool

@dataclass
class CommerceContract:
    contract_id: str
    client_name: str
    contractor_name: str
    total_amount: float
    currency: str
    line_items: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    paypal_order_id: Optional[str] = None
    status: str = "DRAFT" # DRAFT, APPROVED, FUNDED, SETTLED

class NegotiatorAgent:
    """Parses natural language requests into structured commerce agreements."""
    def parse_intent(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        # Extract currency
        currency = "USD"
        if "eur" in text_lower or "€" in text:
            currency = "EUR"
        elif "gbp" in text_lower or "£" in text:
            currency = "GBP"
        elif "bdt" in text_lower or "taka" in text_lower:
            currency = "BDT"

        # Extract amount
        amount_matches = re.findall(r"[\$€£]?\s*(\d+(?:\.\d{1,2})?)", text)
        amount = 100.0
        if amount_matches:
            try:
                # Find the most relevant numeric amount
                valid_amounts = [float(a) for a in amount_matches if float(a) > 0]
                if valid_amounts:
                    amount = valid_amounts[0]
            except ValueError:
                amount = 100.0

        # Extract description / deliverables
        deliverable = "Autonomous AI Software Engineering Deliverable"
        if "design" in text_lower or "ui" in text_lower:
            deliverable = "UI/UX Interactive System Design & Prototype"
        elif "consulting" in text_lower or "audit" in text_lower:
            deliverable = "Architecture & Security Audit Consulting"
        elif "backend" in text_lower or "api" in text_lower:
            deliverable = "Production Backend API & PayPal Webhook Integration"
        elif "model" in text_lower or "ai" in text_lower:
            deliverable = "Custom Edge AI Inference Engine & Fine-Tuning"

        items = [
            LineItem(
                description=f"Milestone 1: {deliverable} - Core Implementation",
                amount=round(amount * 0.6, 2),
                milestone_id="M1"
            ),
            LineItem(
                description=f"Milestone 2: Final Integration & QA Verification",
                amount=round(amount * 0.4, 2),
                milestone_id="M2"
            )
        ]

        return {
            "title": deliverable,
            "total_amount": amount,
            "currency": currency,
            "line_items": [asdict(item) for item in items]
        }

class RiskAuditAgent:
    """Autonomous fraud detection and transaction velocity evaluator."""
    def evaluate_risk(self, amount: float, client_history_count: int = 5, velocity_score: float = 0.12) -> RiskEvaluation:
        # Algorithmic risk heuristics
        flags = []
        score = 94.0 # Base trusted high score
        
        if amount > 5000:
            score -= 15.0
            flags.append("LARGE_TRANSACTION_VALUE: Manual secondary 2FA recommended")
        if amount > 10000:
            score -= 25.0
            flags.append("TIER_1_ESCROW_REQUIRED: Holding period advised")

        if client_history_count < 2:
            score -= 8.0
            flags.append("NEW_COUNTERPARTY: First-time client on protocol")
            
        if velocity_score > 0.8:
            score -= 30.0
            flags.append("HIGH_VELOCITY_BURST: Rapid successive order creations")

        score = max(10.0, min(100.0, score))
        
        if score >= 85:
            level = "LOW"
            hold = 0
            instant = True
        elif score >= 65:
            level = "MEDIUM"
            hold = 24
            instant = True
        elif score >= 40:
            level = "HIGH"
            hold = 72
            instant = False
        else:
            level = "CRITICAL"
            hold = 168
            instant = False

        return RiskEvaluation(
            trust_score=round(score, 1),
            risk_level=level,
            anomaly_flags=flags,
            max_recommended_hold_hours=hold,
            authorized_for_instant_payout=instant
        )

class SettlementAgent:
    """Orchestrates contract lifecycle, escrow locks, and PayPal Orders v2 settlement."""
    def __init__(self, paypal_client):
        self.paypal = paypal_client
        self.negotiator = NegotiatorAgent()
        self.risk_auditor = RiskAuditAgent()
        self.contracts: Dict[str, CommerceContract] = {}

    def process_natural_language_request(self, user_prompt: str, client_id: str = "Client-Alpha") -> Dict[str, Any]:
        """Full end-to-end multi-agent execution pipeline."""
        start_ts = time.perf_counter()
        
        # 1. Negotiate & Parse
        parsed = self.negotiator.parse_intent(user_prompt)
        
        # 2. Risk Audit
        risk = self.risk_auditor.evaluate_risk(parsed["total_amount"])
        
        # 3. Create PayPal Order
        order = self.paypal.create_order(
            amount=parsed["total_amount"],
            currency=parsed["currency"],
            description=f"AgentFlow: {parsed['title']}"
        )
        
        contract_id = f"CTR-{int(time.time())}-{order['id'][-6:]}"
        
        contract = CommerceContract(
            contract_id=contract_id,
            client_name=client_id,
            contractor_name="Mushfiqur Rahim / Autonomous Agent (L)",
            total_amount=parsed["total_amount"],
            currency=parsed["currency"],
            line_items=parsed["line_items"],
            risk_assessment=asdict(risk),
            paypal_order_id=order.get("id"),
            status="AWAITING_PAYMENT"
        )
        self.contracts[contract_id] = contract

        elapsed_ms = (time.perf_counter() - start_ts) * 1000

        return {
            "contract": asdict(contract),
            "paypal_order": order,
            "pipeline_latency_ms": round(elapsed_ms, 2),
            "agent_consensus": {
                "negotiator": "APPROVED_TERMS",
                "risk_auditor": risk.risk_level,
                "settlement": "ORDER_ACTIVE"
            }
        }
