from django import forms
from .models import Action, Campaign, Donation, Expense

class OwnershipEnforcedModelForm(forms.ModelForm):
    """Ensure a volunteer can only pick their own Action or Campaign in FKs."""
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            if "owner" in self.fields:
                self.fields["owner"].queryset = self.fields["owner"].queryset.filter(id=user.id)
            if "source_action" in self.fields:
                self.fields["source_action"].queryset = self.fields["source_action"].queryset.filter(owner=user)
            if "source_campaign" in self.fields:
                self.fields["source_campaign"].queryset = self.fields["source_campaign"].queryset.filter(owner=user)
            if "related_action" in self.fields:
                self.fields["related_action"].queryset = self.fields["related_action"].queryset.filter(owner=user)
            if "related_campaign" in self.fields:
                self.fields["related_campaign"].queryset = self.fields["related_campaign"].queryset.filter(owner=user)

class ActionForm(OwnershipEnforcedModelForm):
    class Meta:
        model = Action
        fields = "__all__"

class CampaignForm(OwnershipEnforcedModelForm):
    class Meta:
        model = Campaign
        fields = "__all__"

class DonationForm(OwnershipEnforcedModelForm):
    class Meta:
        model = Donation
        fields = "__all__"

class ExpenseForm(OwnershipEnforcedModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
