"""
Asset Generation Script for PayPal-AgentFlow.
Generates 1200x630 submission banner and 5-slide PDF pitch deck.
Architect: Mushfiqur Rahim & L
"""

import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

DIR = os.path.dirname(__file__)

def generate_banner():
    w, h = 1200, 630
    img = Image.new('RGB', (w, h), color=(10, 14, 26))
    draw = ImageDraw.Draw(img)

    # Grid background
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(18, 25, 45), width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=(18, 25, 45), width=1)

    # PayPal Blue Top Stripe
    draw.rectangle([0, 0, w, 8], fill=(0, 112, 186))
    draw.rectangle([50, 50, w-50, h-50], outline=(30, 42, 70), width=2)

    # Corner Accents
    c_len = 30
    corners = [(50, 50), (w-50, 50), (50, h-50), (w-50, h-50)]
    for cx, cy in corners:
        dx = c_len if cx == 50 else -c_len
        dy = c_len if cy == 50 else -c_len
        draw.line([(cx, cy), (cx + dx, cy)], fill=(0, 112, 186), width=4)
        draw.line([(cx, cy), (cx, cy + dy)], fill=(0, 112, 186), width=4)

    # Badge
    draw.rounded_rectangle([90, 100, 390, 140], radius=8, fill=(0, 112, 186))
    draw.text((110, 112), 'PAYPAL AI HACKATHON 2026', fill=(255, 255, 255))

    # Title & Subtitle
    try:
        font_lg = ImageFont.truetype('arialbd.ttf', 56)
        font_sub = ImageFont.truetype('arial.ttf', 24)
        font_stat = ImageFont.truetype('arialbd.ttf', 20)
    except:
        font_lg = font_sub = font_stat = None

    draw.text((90, 170), 'PayPal-AgentFlow', fill=(255, 255, 255), font=font_lg)
    draw.text((90, 250), 'Autonomous Multi-Agent Commerce & Escrow Protocol', fill=(160, 180, 215), font=font_sub)
    draw.text((90, 295), 'Powered by PayPal Orders v2 Sandbox API & Tri-Agent Risk Engine', fill=(16, 185, 129), font=font_sub)

    # 4 Feature Metric Cards
    stats = [
        ('SETTLEMENT', 'Instant / 0h Hold', (16, 185, 129)),
        ('AI ORCHESTRATION', 'Tri-Agent Consensus', (0, 112, 186)),
        ('API INTEGRATION', 'PayPal Orders v2', (255, 180, 0)),
        ('TRUST SCORE', '96.5% Low Anomaly', (100, 200, 255))
    ]

    card_w = 235
    for i, (label, val, col) in enumerate(stats):
        bx = 90 + i * (card_w + 15)
        by = 410
        draw.rounded_rectangle([bx, by, bx+card_w, by+120], radius=10, fill=(15, 22, 38), outline=(35, 48, 80), width=2)
        draw.rectangle([bx+15, by+15, bx+25, by+25], fill=col)
        draw.text((bx+35, by+15), label, fill=(130, 150, 185))
        draw.text((bx+20, by+55), val, fill=(255, 255, 255), font=font_stat)

    banner_path = os.path.join(DIR, 'banner.png')
    img.save(banner_path)
    img.save(r'C:\Users\mushfiqur\Desktop\PayPal_AgentFlow_Banner.png')
    print('Banner saved to:', banner_path)

def generate_pitch_deck():
    pdf_path = os.path.join(DIR, 'PayPal_AgentFlow_Pitch_Deck.pdf')
    w, h = landscape(letter) # 792 x 612
    c = canvas.Canvas(pdf_path, pagesize=(w, h))

    slides = [
        {
            'title': 'PayPal-AgentFlow',
            'subtitle': 'Autonomous Multi-Agent Commerce & Escrow Protocol',
            'bullets': [
                'Submission: PayPal AI Hackathon 2026 (Devpost)',
                'Architects: Mushfiqur Rahim & L',
                'Core Tech: PayPal Orders v2 API + ReAct Multi-Agent Consensus + FastAPI',
                'Vision: Enabling autonomous AI agents to negotiate, invoice, and settle payments with zero friction.'
            ]
        },
        {
            'title': 'The Problem: Agent-to-Agent Commerce Friction',
            'subtitle': 'Why Traditional Checkouts Break in the Autonomous Agent Era',
            'bullets': [
                'Manual Invoice Bottlenecks: Freelancers and AI services lose hours generating manual invoices.',
                'Dispute & Fraud Risk: Freelance milestones suffer from chargeback fraud and payment delays.',
                'Agentic Economy Deficit: Modern LLMs can write code, but cannot legally or safely hold and release funds.',
                'Need for Protocol: A secure bridge connecting autonomous agents with regulated banking rails (PayPal).'
            ]
        },
        {
            'title': 'The Solution: PayPal Orders v2 Integration',
            'subtitle': 'Tri-Agent Autonomous Workflow with Deterministic Risk Auditing',
            'bullets': [
                'Negotiator Agent: Parses natural language statements into formal milestone agreements.',
                'RiskAudit Agent: Evaluates counterparty trust score (0-100) and checks transaction velocity.',
                'Settlement Agent: Interacts with PayPal Orders v2 API to create capture-intent orders in seconds.',
                'PayPal Smart SDK: Renders official PayPal buttons directly in the operator HUD.'
            ]
        },
        {
            'title': 'Interactive HUD & Developer Experience',
            'subtitle': 'Zero-Friction Live Demo Deployed Globally on GitHub Pages',
            'bullets': [
                'Standalone WebGL/Canvas HUD: Live transaction stream, risk telemetry, and PayPal SDK buttons.',
                'Zero-Friction Sandbox Fallback: Judges can test full checkout flows immediately without credentials.',
                'Deterministic Latency: Sub-10ms pipeline execution from prompt to checkout button.',
                'Modular REST API: Easily integrated into any existing e-commerce or SaaS platform.'
            ]
        },
        {
            'title': 'Roadmap & Production Expansion',
            'subtitle': 'From Hackathon Prototype to Global AI Commerce Standard',
            'bullets': [
                'Phase 1 (Complete): Orders v2 Sandbox client, Tri-agent consensus, interactive HUD, test suite.',
                'Phase 2: PayPal Payouts API integration for automated contractor micro-distributions.',
                'Phase 3: Webhook event verification for automated escrow release upon GitHub commit / PR merge.',
                'Live Repository: https://github.com/MD-Mushfiqur123/PayPal-AgentFlow'
            ]
        }
    ]

    for s in slides:
        # Background
        c.setFillColor(colors.HexColor('#0A0E1A'))
        c.rect(0, 0, w, h, fill=True, stroke=False)

        # Top PayPal blue bar
        c.setFillColor(colors.HexColor('#0070BA'))
        c.rect(0, h-8, w, 8, fill=True, stroke=False)

        # Header
        c.setFillColor(colors.white)
        c.setFont('Helvetica-Bold', 26)
        c.drawString(60, h-70, s['title'])

        c.setFillColor(colors.HexColor('#0070BA'))
        c.setFont('Helvetica-Bold', 13)
        c.drawString(60, h-98, s['subtitle'])

        # Divider
        c.setStrokeColor(colors.HexColor('#1E293B'))
        c.setLineWidth(1)
        c.line(60, h-115, w-60, h-115)

        # Bullets
        c.setFont('Helvetica', 14)
        y = h - 170
        for b in s['bullets']:
            c.setFillColor(colors.HexColor('#0070BA'))
            c.circle(75, y+5, 4, fill=True, stroke=False)
            c.setFillColor(colors.HexColor('#E2E8F0'))
            c.drawString(95, y, b)
            y -= 48

        # Footer
        c.setFillColor(colors.HexColor('#64748B'))
        c.setFont('Helvetica', 10)
        c.drawString(60, 30, 'PAYPAL AI HACKATHON 2026 | PayPal-AgentFlow Submission')
        c.drawRightString(w-60, 30, 'MD-Mushfiqur123 / L')

        c.showPage()

    c.save()
    desktop_copy = r'C:\Users\mushfiqur\Desktop\PayPal_AgentFlow_Pitch_Deck.pdf'
    import shutil
    shutil.copyfile(pdf_path, desktop_copy)
    print('Pitch Deck saved to:', pdf_path)

if __name__ == '__main__':
    generate_banner()
    generate_pitch_deck()
