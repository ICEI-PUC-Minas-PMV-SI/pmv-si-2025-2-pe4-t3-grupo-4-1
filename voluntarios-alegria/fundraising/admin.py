# fundraising/admin.py
from django.contrib import admin
from django.http import HttpResponse
from django.utils.encoding import smart_str
import csv
from django.contrib.auth import get_user_model
from django.db.models import Q  # <-- add this
from core.mixins import user_is_admin
from .models import Action, Campaign, Donation, Expense
from .forms import ActionForm, CampaignForm, DonationForm, ExpenseForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class ReadonlyInline(admin.TabularInline):
    can_delete = False
    extra = 0

class DonationsInline(ReadonlyInline):
    model = Donation
    fields = ("timestamp", "amount", "method", "source_action", "source_campaign", "created_at", "updated_at")
    readonly_fields = ("timestamp", "amount", "method", "source_action", "source_campaign", "created_at", "updated_at")

class ExpensesInline(ReadonlyInline):
    model = Expense
    fields = ("paid_at", "amount", "related_action", "related_campaign", "created_at", "updated_at")
    readonly_fields = ("paid_at", "amount", "related_action", "related_campaign", "created_at", "updated_at")

def export_as_csv(modeladmin, request, queryset, fields, filename):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
    writer = csv.writer(response)
    writer.writerow(fields)
    for obj in queryset:
        writer.writerow([smart_str(getattr(obj, f)) for f in fields])
    return response

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    form = ActionForm
    list_display = ("title", "category", "status", "goal_amount", "total_donations", "total_expenses", "created_at")
    list_filter = ("status", "category",)  # valid for Action (has category)
    search_fields = ("title", "description")
    readonly_fields = ("total_donations", "total_expenses", "progress_percent")
    inlines = [DonationsInline, ExpensesInline]
    actions = ["export_actions"]

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def total_donations(self, obj):
        return obj.total_donations
    total_donations.short_description = _("Total de Doações")  # Tradução do campo no Admin

    def total_expenses(self, obj):
        return obj.total_expenses
    total_expenses.short_description = _("Total de Despesas")  # Tradução do campo no Admin

    def progress_percent(self, obj):
        return f"{obj.progress_percent:.2f}%"
    progress_percent.short_description = _("Percentual de Progresso")  # Tradução do campo no Admin

    def export_actions(self, request, queryset):
        fields = ["id", "title", "category", "status", "goal_amount", "owner_id", "created_at", "updated_at"]
        return export_as_csv(self, request, queryset, fields, "actions")

@admin.register(Campaign)
class CampaignAdmin(ActionAdmin):
    form = CampaignForm
    list_display = ("name", "status", "goal_amount", "total_donations", "total_expenses", "created_at")
    # Campaign does NOT have "category" -> override list_filter to remove it
    list_filter = ("status", )
    search_fields = ("name", "description")


    def export_actions(self, request, queryset):
        fields = ["id", "name", "status", "goal_amount", "owner_id", "created_at", "updated_at"]
        return export_as_csv(self, request, queryset, fields, "campaigns")

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    form = DonationForm
    list_display = ("timestamp", "amount", "method", "source_action", "source_campaign", "created_by")
    list_filter = ("method", )
    search_fields = ("donor_name", "donor_email", "description")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_is_admin(request.user):
            return qs
        return qs.filter(Q(source_action__owner=request.user) | Q(source_campaign__owner=request.user))

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        if not user_is_admin(request.user):
            if obj.source_action and obj.source_action.owner_id != request.user.id:
                from django.core.exceptions import ValidationError
                raise ValidationError("Volunteers can only register donations to their own Actions.")
            if obj.source_campaign and obj.source_campaign.owner_id != request.user.id:
                from django.core.exceptions import ValidationError
                raise ValidationError("Volunteers can only register donations to their own Campaigns.")
        super().save_model(request, obj, form, change)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseForm
    list_display = ("title", "amount", "paid_at", "related_action", "related_campaign", "created_by")
    # Expense does NOT have "method" or "currency" -> use valid filters
    list_filter = ("paid_at", "related_action", "related_campaign")
    search_fields = ("title", "description")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_is_admin(request.user):
            return qs
        return qs.filter(Q(related_action__owner=request.user) | Q(related_campaign__owner=request.user))

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        if not user_is_admin(request.user):
            if obj.related_action and obj.related_action.owner_id != request.user.id:
                from django.core.exceptions import ValidationError
                raise ValidationError("Volunteers can only register expenses for their own Actions.")
            if obj.related_campaign and obj.related_campaign.owner_id != request.user.id:
                from django.core.exceptions import ValidationError
                raise ValidationError("Volunteers can only register expenses for their own Campaigns.")
        super().save_model(request, obj, form, change)
