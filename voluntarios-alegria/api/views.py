from rest_framework.generics import ListAPIView
from fundraising.models import Campaign, Action, Donation, Expense, Beneficiary
from .serializers import CampaignSerializer, ActionSerializer, DonationSerializer, ExpenseSerializer, BeneficiarySerializer
from django_filters import rest_framework as filters
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Filtro para datas (se necessário)
class DateFilterSet(filters.FilterSet):
    date_from = filters.DateFilter(field_name="start_date", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="end_date", lookup_expr="lte")

class CampaignListView(ListAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    filterset_class = DateFilterSet
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ActionListView(ListAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filterset_class = DateFilterSet
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class DonationListView(ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filterset_class = DateFilterSet
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ExpenseListView(ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filterset_class = DateFilterSet
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class BeneficiaryListView(ListAPIView):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    filterset_class = DateFilterSet
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]