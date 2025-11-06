from rest_framework import serializers
from fundraising.models import Campaign, Action, Donation, Expense

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id", "name", "goal_amount", "start_date", "end_date", "status", "total_donations", "total_expenses", "progress_percent"]

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "title", "category", "goal_amount", "start_date", "end_date", "status", "total_donations", "total_expenses", "progress_percent"]

class DonationSerializer(serializers.ModelSerializer):
    campaign_id = serializers.IntegerField(source="source_campaign.id", required=False, allow_null=True)  # Torna o campo de campanha opcional
    action_id = serializers.IntegerField(source="source_action.id", required=False, allow_null=True)  # Torna o campo de ação opcional

    class Meta:
        model = Donation
        fields = ["id", "donor_name", "donor_email", "amount", "method", "timestamp", "campaign_id", "action_id"]

    def validate(self, attrs):
        # Se não houver ação nem campanha, levanta um erro
        if not attrs.get("source_action") and not attrs.get("source_campaign"):
            raise serializers.ValidationError("É necessário definir exatamente uma das opções: source_action ou source_campaign.")
        return attrs

class ExpenseSerializer(serializers.ModelSerializer):
    action_id = serializers.IntegerField(source="related_action.id", required=False, allow_null=True)  # Torna o campo de ação opcional
    campaign_id = serializers.IntegerField(source="related_campaign.id", required=False, allow_null=True)  # Torna o campo de campanha opcional
    class Meta:
        model = Expense
        fields = ["id", "title", "description", "amount", "paid_at", "action_id", "campaign_id"]
