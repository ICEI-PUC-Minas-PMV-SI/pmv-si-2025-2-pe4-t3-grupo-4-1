from datetime import datetime
from typing import Dict, Iterable, Optional, Literal
from django.db.models import Sum, Count, F, Q, QuerySet, DateField, DateTimeField
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from .models import Action, Campaign, Donation, Expense

def compute_action_totals(action_id: int) -> Dict:
    a = Action.objects.get(pk=action_id)
    return {
        "action_id": a.id,
        "title": a.title,
        "total_donations": a.total_donations,
        "total_expenses": a.total_expenses,
        "progress_percent": a.progress_percent,
    }

def compute_campaign_totals(campaign_id: int) -> Dict:
    c = Campaign.objects.get(pk=campaign_id)
    return {
        "campaign_id": c.id,
        "name": c.name,
        "total_donations": c.total_donations,
        "total_expenses": c.total_expenses,
        "progress_percent": c.progress_percent,
    }

Granularity = Literal["day", "week", "month"]

def _trunc_for(granularity: Granularity):
    return {"day": TruncDay, "week": TruncWeek, "month": TruncMonth}[granularity]

def aggregate_timeseries(model, date_field: str, group_by: Iterable[str], granularity: Granularity, filters: Optional[Q] = None) -> QuerySet:
    Trunc = _trunc_for(granularity)
    qs = model.objects.all()
    if filters is not None:
        qs = qs.filter(filters)
    return qs.annotate(
        date_key=Trunc(date_field)
    ).values(
        "date_key", *group_by
    ).annotate(
        amount_sum=Sum("amount"), count=Count("id")
    ).order_by("date_key")

def validate_single_link(obj, action_field: str, campaign_field: str) -> None:
    a = getattr(obj, action_field)
    c = getattr(obj, campaign_field)
    if bool(a) == bool(c):
        raise ValueError("Exactly one relation must be set.")
