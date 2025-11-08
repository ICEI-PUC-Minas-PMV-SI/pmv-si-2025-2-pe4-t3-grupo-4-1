from rest_framework import serializers
from fundraising.models import Campaign, Action, Donation, Expense, Beneficiary

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id", "name", "goal_amount", "start_date", "end_date", "status", "total_donations", "total_expenses", "progress_percent"]

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "title", "category", "goal_amount", "start_date", "end_date", "status", "total_donations", "total_expenses", "progress_percent"]

class DonationSerializer(serializers.ModelSerializer):
    campaign_id = serializers.IntegerField(source="source_campaign.id", required=False, allow_null=True)

    class Meta:
        model = Donation
        fields = ["id", "donor_name", "donor_email", "amount", "method", "timestamp", "campaign_id"]

    def validate(self, attrs):
        if not attrs.get("source_campaign"):
            raise serializers.ValidationError("É necessário definir exatamente uma das opções: source_action ou source_campaign.")
        return attrs

class ExpenseSerializer(serializers.ModelSerializer):
    campaign_id = serializers.IntegerField(source="related_campaign.id", required=False, allow_null=True)
    class Meta:
        model = Expense
        fields = ["id", "title", "description", "amount", "paid_at", "campaign_id"]


class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ["id", "name", "description", "contact_info"]