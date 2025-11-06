from django.urls import path
from .views import CampaignListView, ActionListView, DonationListView, ExpenseListView

urlpatterns = [
    path("export/campanhas/", CampaignListView.as_view(), name="export-campanhas"),
    path("export/acoes/", ActionListView.as_view(), name="export-acoes"),
    path("export/doacoes/", DonationListView.as_view(), name="export-doacoes"),
    path("export/despesas/", ExpenseListView.as_view(), name="export-despesas"),
]
