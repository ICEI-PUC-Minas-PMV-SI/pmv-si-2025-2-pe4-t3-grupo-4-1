from django.db import models
from django.db.models import Sum, Q, CheckConstraint
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from core.models import AuditModel
from core.validators import validate_attachment
from django.utils.translation import gettext_lazy as _

User = get_user_model()

CATEGORY_CHOICES = [
    ("Senior", _("Idosos")),
    ("Animal", _("Animais")),
    ("Child", _("Crianças")),
    ("Environmental", _("Ambiental")),
]

STATUS_CHOICES = [
    ("draft", _("Rascunho")),
    ("active", _("Ativo")),
    ("done", _("Concluído")),
    ("archived", _("Arquivado")),
]

class Action(AuditModel):
    title = models.CharField(_("Título"), max_length=200)
    description = models.TextField(_("Descrição"), blank=True)
    category = models.CharField(_("Categoria"), max_length=20, choices=CATEGORY_CHOICES)
    goal_amount = models.DecimalField(_("Meta"), max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField(_("Data de Início"))
    end_date = models.DateField(_("Data de Término"), null=True, blank=True)
    status = models.CharField(_("Sitação"), max_length=16, choices=STATUS_CHOICES, default="draft")

    class Meta:
        verbose_name = _("ação")
        verbose_name_plural = _("ações")
        indexes = [models.Index(fields=["status", "category"])]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def total_donations(self):
        return self.donations.aggregate(s=Sum("amount"))["s"] or 0

    @property
    def total_expenses(self):
        return self.expenses.aggregate(s=Sum("amount"))["s"] or 0


    @property
    def progress_percent(self):
        if not self.goal_amount or self.goal_amount <= 0:
            return 0
        return float((self.total_donations / self.goal_amount) * 100)

    def __str__(self):
        return self.title


class Campaign(AuditModel):
    name = models.CharField(_("Nome"), max_length=200)
    description = models.TextField(_("Descrição"), blank=True)
    goal_amount = models.DecimalField(_("Meta"), max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField(_("Data de Início"))
    end_date = models.DateField(_("Data de Término"), null=True, blank=True)
    status = models.CharField(_("Situação"), max_length=16, choices=STATUS_CHOICES, default="draft")

    class Meta:
        verbose_name = _("campanha")
        verbose_name_plural = _("campanhas")
        indexes = [models.Index(fields=["status",])]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def total_donations(self):
        direct = self.donations.aggregate(s=Sum("amount"))["s"] or 0
        via_actions = self.actions.aggregate(s=Sum("donations__amount"))["s"] or 0
        return direct + via_actions

    @property
    def total_expenses(self):
        direct = self.expenses.aggregate(s=Sum("amount"))["s"] or 0
        via_actions = self.actions.aggregate(s=Sum("expenses__amount"))["s"] or 0
        return direct + via_actions

    @property
    def progress_percent(self):
        if not self.goal_amount or self.goal_amount <= 0:
            return 0
        return float((self.total_donations / self.goal_amount) * 100)

    def __str__(self):
        return self.name


class Donation(AuditModel):
    donor_name = models.CharField(_("Nome do doador"),max_length=200, blank=True)
    donor_email = models.EmailField(_("Email do doador"), blank=True)
    amount = models.DecimalField(_("Valor"), max_digits=12, decimal_places=2)
    description = models.TextField(_("Descrição"), blank=True)
    method = models.CharField(_("Método"), max_length=20, choices=[
        ("pix", "Pix"), ("credit_card", _("Cartão de Crédito")),
        ("cash", "Dinheiro"), ("bank_transfer", "Transferência Bancária"), ("other", "Outro")
    ])
    timestamp = models.DateTimeField()
    source_action = models.ForeignKey(Action, null=True, blank=True, on_delete=models.CASCADE, related_name="donations", verbose_name=_("Ação relacionada"))
    source_campaign = models.ForeignKey(Campaign, null=True, blank=True, on_delete=models.CASCADE, related_name="donations", verbose_name=_("Campanha relacionada"))

    class Meta:
        constraints = [
            CheckConstraint(
                check=(
                    (Q(source_action__isnull=False) & Q(source_campaign__isnull=True)) |
                    (Q(source_action__isnull=True) & Q(source_campaign__isnull=False))
                ),
                name="donation_one_source",
            )
        ]
        indexes = [models.Index(fields=["timestamp", "method",])]
        verbose_name = _("doação")
        verbose_name_plural = _("doações")

    def clean(self):
        if bool(self.source_action) == bool(self.source_campaign):
            raise ValidationError(_("É necessário definir exatamente uma das opções: source_action ou source_campaign."))
        if self.amount is not None and self.amount < 0:
            raise ValidationError(_("O valor não pode ser negativo."))


class Expense(AuditModel):
    title = models.CharField(_("Título"), max_length=200)
    description = models.TextField(_("Descrição"), blank=True)
    amount = models.DecimalField(_("Valor"), max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(_("Data de Pagamento"))
    related_action = models.ForeignKey(Action, null=True, blank=True, on_delete=models.CASCADE, related_name="expenses", verbose_name=_("Ação relacionada") )
    related_campaign = models.ForeignKey(Campaign, null=True, blank=True, on_delete=models.CASCADE, related_name="expenses", verbose_name=_("Campanha relacionada"))
    receipt = models.FileField(_("Comprovante"), upload_to="receipts/", validators=[validate_attachment])

    class Meta:
        constraints = [
            CheckConstraint(
                check=(
                    (Q(related_action__isnull=False) & Q(related_campaign__isnull=True)) |
                    (Q(related_action__isnull=True) & Q(related_campaign__isnull=False))
                ),
                name="expense_one_relation",
            )
        ]
        indexes = [models.Index(fields=["paid_at"])]
        verbose_name = _("despesa")
        verbose_name_plural = _("despesas")

    def clean(self):
        if bool(self.related_action) == bool(self.related_campaign):
            raise ValidationError(_("É necessário definir exatamente uma das opções: ação ou campanha."))
        if self.amount is not None and self.amount < 0:
            raise ValidationError(_("O valor não pode ser negativo."))
