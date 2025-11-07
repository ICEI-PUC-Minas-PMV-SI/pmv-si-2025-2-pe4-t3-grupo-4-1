import csv
from django.conf import settings
from fundraising.models import Campaign, Action, Donation, Expense
from decimal import Decimal
from django.utils import timezone

# Função para converter Decimal para float
def convert_decimal_to_float(obj):
    if isinstance(obj, dict):
        return {key: convert_decimal_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal_to_float(item) for item in obj]
    elif isinstance(obj, Decimal):  # Convertendo Decimal para float
        return float(obj)
    return obj

# Função para escrever todos os dados em um único arquivo CSV
def write_all_to_csv(filename, campaigns_data, actions_data, donations_data, expenses_data):
    # Combinando todos os dados em uma lista única
    all_data = campaigns_data + actions_data + donations_data + expenses_data

    # Definir o nome das colunas (cabeçalho)
    fieldnames = [
        "Type", "Title", "Category", "GoalAmount", "TotalDonations", "StartDate", "EndDate",
        "DonorName", "DonorEmail", "Amount", "Timestamp", "RelatedAction", "RelatedCampaign"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Escreve o cabeçalho
        writer.writerows(all_data)  # Escreve os dados combinados

# Função de anonimização de dados
def anonymize_data(name, email):
    # Simulação de anonimização
    anonymized_name = f"User_{hash(name)}"
    anonymized_email = f"anon_{hash(email)}@domain.com"
    return anonymized_name, anonymized_email

# Função principal que será executada periodicamente
def export_data_to_power_bi():
    # 1. Exporta dados de Campanhas
    campaigns = Campaign.objects.all()
    campaigns_data = []
    for campaign in campaigns:
        campaigns_data.append({
            "Type": "Campaign",
            "Title": campaign.name,
            "Category": campaign.category,
            "GoalAmount": campaign.goal_amount,
            "TotalDonations": campaign.total_donations,
            "StartDate": campaign.start_date.strftime("%Y-%m-%d"),
            "EndDate": campaign.end_date.strftime("%Y-%m-%d") if campaign.end_date else "N/A",
            "DonorName": "",
            "DonorEmail": "",
            "Amount": "",
            "Timestamp": "",
            "RelatedAction": "",
            "RelatedCampaign": ""
        })

    # 2. Exporta dados de Ações
    actions = Action.objects.all()
    actions_data = []
    for action in actions:
        actions_data.append({
            "Type": "Action",
            "Title": action.title,
            "Category": action.category,
            "GoalAmount": action.goal_amount,
            "TotalDonations": action.total_donations,
            "StartDate": action.start_date.strftime("%Y-%m-%d"),
            "EndDate": action.end_date.strftime("%Y-%m-%d") if action.end_date else "N/A",
            "DonorName": "",
            "DonorEmail": "",
            "Amount": "",
            "Timestamp": "",
            "RelatedAction": "",
            "RelatedCampaign": action.related_campaign.name if action.related_campaign else "N/A"
        })

    # 3. Exporta dados de Doações
    donations = Donation.objects.all()
    donations_data = []
    for donation in donations:
        anonymized_name, anonymized_email = anonymize_data(donation.donor_name, donation.donor_email)
        donations_data.append({
            "Type": "Donation",
            "Title": donation.source_campaign.name if donation.source_campaign else "N/A",
            "Category": "",
            "GoalAmount": "",
            "TotalDonations": "",
            "StartDate": "",
            "EndDate": "",
            "DonorName": anonymized_name,
            "DonorEmail": anonymized_email,
            "Amount": donation.amount,
            "Timestamp": donation.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "RelatedAction": "",
            "RelatedCampaign": ""
        })

    # 4. Exporta dados de Despesas
    expenses = Expense.objects.all()
    expenses_data = []
    for expense in expenses:
        expenses_data.append({
            "Type": "Expense",
            "Title": expense.title,
            "Category": "",
            "GoalAmount": "",
            "TotalDonations": "",
            "StartDate": "",
            "EndDate": "",
            "DonorName": "",
            "DonorEmail": "",
            "Amount": expense.amount,
            "Timestamp": expense.paid_at.strftime("%Y-%m-%d %H:%M:%S"),
            "RelatedAction": expense.related_action.title if expense.related_action else "N/A",
            "RelatedCampaign": expense.related_campaign.name if expense.related_campaign else "N/A"
        })

    # 5. Escreve todos os dados no CSV
    write_all_to_csv('all_data.csv', campaigns_data, actions_data, donations_data, expenses_data)

    print("Dados exportados para CSV com sucesso.")
