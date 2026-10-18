"""
FastAPI Server for PayPal-AgentFlow.
Provides real-time endpoints for multi-agent conversational commerce, risk scoring, and PayPal Orders v2 integration.
Architect: Mushfiqur Rahim & L
"""

import os
import time
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from paypal_client import PayPalClient
from agent_engine import SettlementAgent

app = FastAPI(
    title="PayPal-AgentFlow API",
    description="Autonomous Multi-Agent Escrow & Smart Commerce Protocol on PayPal Orders v2",
    version="1.0.0"
)

# Enable CORS for all origins (allowing GitHub Pages or localhost to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate PayPal Client and Multi-Agent Settlement Coordinator
paypal_client = PayPalClient()
settlement_agent = SettlementAgent(paypal_client)

# In-Memory Transaction Ledger
LEDGER = []

class ChatRequest(BaseModel):
    message: str
    client_name: Optional[str] = "Global Merchant"

class OrderCreateRequest(BaseModel):
    amount: float
    currency: Optional[str] = "USD"
    description: Optional[str] = "Direct AgentFlow Invoice"

class OrderCaptureRequest(BaseModel):
    order_id: str

@app.get("/api/health")
def health_check():
    return {
        "status": "ONLINE",
        "service": "PayPal-AgentFlow",
        "mode": "Live PayPal Sandbox v2" if paypal_client.is_configured else "Sandbox-Emulated (Zero-Friction)",
        "paypal_configured": paypal_client.is_configured,
        "timestamp": time.time(),
        "architect": "Mushfiqur Rahim & L"
    }

@app.post("/api/chat")
def process_chat(req: ChatRequest):
    """Processes conversational prompt through Negotiator, Risk Audit, and Settlement Agents."""
    if not req.message or len(req.message.strip()) < 3:
        raise HTTPException(status_code=400, detail="Message too short")

    result = settlement_agent.process_natural_language_request(req.message, req.client_name)
    
    # Record to ledger
    ledger_entry = {
        "timestamp": time.time(),
        "type": "CONVERSATIONAL_INVOICE",
        "contract_id": result["contract"]["contract_id"],
        "order_id": result["paypal_order"]["id"],
        "amount": result["contract"]["total_amount"],
        "currency": result["contract"]["currency"],
        "trust_score": result["contract"]["risk_assessment"]["trust_score"],
        "risk_level": result["contract"]["risk_assessment"]["risk_level"],
        "status": result["contract"]["status"]
    }
    LEDGER.append(ledger_entry)

    return result

@app.post("/api/orders/create")
def create_order(req: OrderCreateRequest):
    """Directly creates a PayPal Order v2."""
    order = paypal_client.create_order(
        amount=req.amount,
        currency=req.currency,
        description=req.description
    )
    
    LEDGER.append({
        "timestamp": time.time(),
        "type": "DIRECT_ORDER",
        "order_id": order["id"],
        "amount": req.amount,
        "currency": req.currency,
        "status": order["status"]
    })
    
    return order

@app.post("/api/orders/capture")
def capture_order(req: OrderCaptureRequest):
    """Captures an approved PayPal Order v2."""
    res = paypal_client.capture_order(req.order_id)
    
    # Update ledger status
    for entry in LEDGER:
        if entry.get("order_id") == req.order_id:
            entry["status"] = "SETTLED"
            
    return res

@app.get("/api/ledger")
def get_ledger():
    """Returns the persistent multi-agent transaction ledger."""
    return {
        "total_transactions": len(LEDGER),
        "transactions": LEDGER[-20:] # Last 20 transactions
    }

@app.get("/", response_class=HTMLResponse)
def serve_root():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>PayPal-AgentFlow API Running</h1><p>Visit /docs for Swagger UI</p>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
