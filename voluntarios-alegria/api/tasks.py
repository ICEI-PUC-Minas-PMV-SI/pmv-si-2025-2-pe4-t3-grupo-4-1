import requests
import json
from decimal import Decimal
from fundraising.models import Campaign, Action, Donation, Expense, Beneficiary
from datetime import datetime

POWER_BI_ENDPOINT = "https://api.powerbi.com/beta/14cbd5a7-ec94-46ba-b314-cc0fc972a161/datasets/7aac548a-fa51-4c32-b3ce-f2421d98360a/rows?language=pt-BR&experience=power-bi&key=Fnd7yOIyvesZQKTCYMgy5dK%2FlgQhMyExZ%2BH8QrN%2F8IRsMFGthclkJLxXS13IEeXGE1CJs9eBjZPjJ88ymiJbng%3D%3D"


# Converte Decimal → float
def to_float(v):
    return float(v) if isinstance(v, Decimal) else v


# Função principal
def export_data_to_power_bi():
    print("Executando às:", datetime.now())

    rows = []

    # -----------------------------
    # 1. CAMPANHAS
    # -----------------------------
    for c in Campaign.objects.all():
        rows.append({
            "id": to_float(c.id),
            "name": c.name,
            "goal_amount": to_float(c.goal_amount),
            "start_date": c.start_date.isoformat(),
            "end_date": c.end_date.isoformat() if c.end_date else None,
            "status": c.status,
            "total_donations": to_float(c.total_donations),
            "total_expenses": to_float(c.total_expenses),
            "progress_porcent": to_float(c.progress_percent),
            "title": c.name,
            "category": c.category,
            "donor_name": "",
            "donor_email": "",
            "method": "",
            "timestamp": "",
            "campaign_id": to_float(c.id)
        })

    # -----------------------------
    # 2. AÇÕES
    # -----------------------------
    for a in Action.objects.all():
        rows.append({
            "id": to_float(a.id),
            "name": a.title,
            "goal_amount": to_float(a.goal_amount),
            "start_date": a.start_date.isoformat(),
            "end_date": a.end_date.isoformat() if a.end_date else None,
            "status": a.status,
            "total_donations": to_float(a.total_donations),
            "total_expenses": to_float(a.total_expenses),
            "progress_percent": to_float(a.progress_percent),
            "title": a.title,
            "category": a.category,
            "donor_name": "",
            "donor_email": "",
            "method": "",
            "timestamp": "",
            "campaign_id": to_float(a.related_campaign.id) if a.related_campaign else None
        })

    # -----------------------------
    # 3. DOAÇÕES
    # -----------------------------
    for d in Donation.objects.all():
        rows.append({
            "id": to_float(d.id),
            "name": "Donation",
            "goal_amount": "",
            "start_date": "",
            "end_date": "",
            "status": "",
            "total_donations": "",
            "total_expenses": "",
            "progress_porcent": "",
            "title": d.source_campaign.name if d.source_campaign else "",
            "category": "",
            "donor_name": d.donor_name,
            "donor_email": d.donor_email,
            "method": d.method,
            "timestamp": d.timestamp.isoformat(),
            "campaign_id": to_float(d.source_campaign.id) if d.source_campaign else None
        })

    # -----------------------------
    # 4. DESPESAS
    # -----------------------------
    for e in Expense.objects.all():
        rows.append({
            "id": to_float(e.id),
            "name": e.title,
            "goal_amount": "",
            "start_date": "",
            "end_date": "",
            "status": "",
            "total_donations": "",
            "total_expenses": to_float(e.amount),
            "progress_porcent": "",
            "title": e.title,
            "category": "",
            "donor_name": "",
            "donor_email": "",
            "method": "",
            "timestamp": e.paid_at.isoformat() if e.paid_at else "",
            "campaign_id": to_float(e.related_campaign.id) if e.related_campaign else None
        })

    # -----------------------------
    # 5. BENEFICIÁRIOS
    # -----------------------------
    for b in Beneficiary.objects.all():
        rows.append({
            "id": to_float(b.id),
            "name": "Beneficiary",
            "goal_amount": "",
            "start_date": "",
            "end_date": "",
            "status": "",
            "total_donations": "",
            "total_expenses": "",
            "progress_porcent": "",
            "title": "",
            "category": "",
            "donor_name": b.name,
            "donor_email": "" ,
            "method": "",
            "timestamp": "",
            "campaign_id": ""
        })

    # -----------------------------
    #  ENVIO PARA O POWER BI
    # -----------------------------
    payload = {"rows": rows}

    response = requests.post(
        POWER_BI_ENDPOINT,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    print("Status Code:", response.status_code)
    print("Resposta:", response.text)

    return response.status_code
