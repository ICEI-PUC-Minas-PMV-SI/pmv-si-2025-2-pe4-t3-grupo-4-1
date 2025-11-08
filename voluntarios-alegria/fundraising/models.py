from django.db import models
from django.db.models import Sum
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
    start_date = models.DateField(_("Data de Início"))
    end_date = models.DateField(_("Data de Término"), null=True, blank=True)
    status = models.CharField(_("Sitação"), max_length=16, choices=STATUS_CHOICES, default="draft")
    people_impacted = models.PositiveIntegerField(default=0)

    beneficiary = models.ForeignKey(
        "fundraising.Beneficiary",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Entidade beneficiada"),
        related_name="actions",
    )

    participants = models.ManyToManyField(
        User,
        related_name="actions_participated",
        verbose_name=_("Participantes"),
        blank=True,
    )

    class Meta:
        verbose_name = _("ação")
        verbose_name_plural = _("ações")
        indexes = [models.Index(fields=["status", "category"])]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def participants_count(self) -> int:
        return self.participants.count()

    def __str__(self):
        return self.title


class Beneficiary(AuditModel):
    name = models.CharField(_("Nome da entidade"), max_length=200)
    contact_person = models.CharField(_("Pessoa de contato"), max_length=150, blank=True)
    phone = models.CharField(_("Telefone"), max_length=20, blank=True)
    email = models.EmailField(_("E-mail"), blank=True)
    address = models.CharField(_("Endereço"), max_length=255, blank=True)
    description = models.TextField(_("Descrição"), blank=True)
    category = models.CharField(
        _("Categoria do beneficiário"),
        max_length=20,
        choices=[
            ("criancas", "Crianças"),
            ("idosos", "Idosos"),
            ("animais", "Animais"),
            ("meio_ambiente", "Meio Ambiente"),
            ("outros", "Outros"),
        ],
        default="outros",
    )

    class Meta:
        verbose_name = _("beneficiário")
        verbose_name_plural = _("beneficiários")
        indexes = [models.Index(fields=["category", "name"])]

    def __str__(self):
        return self.name


class Campaign(AuditModel):
    name = models.CharField(_("Nome"), max_length=200)
    description = models.TextField(_("Descrição"), blank=True)
    category = models.CharField(_("Categoria"), max_length=20, choices=CATEGORY_CHOICES)
    goal_amount = models.DecimalField(_("Meta"), max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField(_("Data de Início"))
    end_date = models.DateField(_("Data de Término"), null=True, blank=True)
    status = models.CharField(_("Situação"), max_length=16, choices=STATUS_CHOICES, default="draft")

    class Meta:
        verbose_name = _("campanha")
        verbose_name_plural = _("campanhas")
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
        return self.name


class Donation(AuditModel):
    donor_name = models.CharField(_("Nome do doador"), max_length=200, blank=True)
    donor_email = models.EmailField(_("Email do doador"), blank=True)
    amount = models.DecimalField(_("Valor"), max_digits=12, decimal_places=2)
    description = models.TextField(_("Descrição"), blank=True)
    method = models.CharField(_("Método"), max_length=20, choices=[
        ("pix", "Pix"), ("credit_card", _("Cartão de Crédito")),
        ("cash", "Dinheiro"), ("bank_transfer", "Transferência Bancária"), ("other", "Outro")
    ])
    timestamp = models.DateTimeField()
    source_campaign = models.ForeignKey(Campaign, null=True, blank=True, on_delete=models.CASCADE, related_name="donations", verbose_name=_("Campanha relacionada"))

    class Meta:
        indexes = [
            models.Index(fields=["timestamp", "method"]),
        ]
        verbose_name = _("doação")
        verbose_name_plural = _("doações")

    def clean(self):
        if not self.source_campaign:
            raise ValidationError(_("É necessário definir exatamente uma Campanha."))
        if self.amount is not None and self.amount < 0:
            raise ValidationError(_("O valor não pode ser negativo."))


class Expense(AuditModel):
    title = models.CharField(_("Título"), max_length=200)
    description = models.TextField(_("Descrição"), blank=True)
    amount = models.DecimalField(_("Valor"), max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(_("Data de Pagamento"))
    related_campaign = models.ForeignKey(Campaign, null=True, blank=True, on_delete=models.CASCADE, related_name="expenses", verbose_name=_("Campanha relacionada"))
    receipt = models.FileField(_("Comprovante"), upload_to="receipts/", blank=True, validators=[validate_attachment])

    class Meta:
        indexes = [models.Index(fields=["paid_at"])]
        verbose_name = _("despesa")
        verbose_name_plural = _("despesas")

    def clean(self):
        if not self.related_campaign:
            raise ValidationError(_("É necessário definir exatamente uma Campanha."))
        if self.amount is not None and self.amount < 0:
            raise ValidationError(_("O valor não pode ser negativo."))
