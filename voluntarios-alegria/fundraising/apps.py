from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate

def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from fundraising.models import Campaign, Donation, Expense, Action, Beneficiary

    # Grupos
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    volunteer_group, _ = Group.objects.get_or_create(name="Voluntario")

    # ContentTypes dos modelos
    models_ct = {
        Campaign: ContentType.objects.get_for_model(Campaign),
        Donation: ContentType.objects.get_for_model(Donation),
        Expense: ContentType.objects.get_for_model(Expense),
        Action: ContentType.objects.get_for_model(Action),
        Beneficiary: ContentType.objects.get_for_model(Beneficiary),
    }

    # Helper para capturar perms
    def perms_for(model):
        ct = models_ct[model]
        return Permission.objects.filter(content_type=ct)

    # ----- Permissões por grupo -----
    # Admin: todas as permissões de todos os modelos (add, change, delete, view)
    admin_perms = []
    for model in models_ct:
        admin_perms += list(perms_for(model))
    admin_group.permissions.set(admin_perms)

    # Voluntário: somente "view_*" e  "add_*" em todos os modelos
    volunteer_perms = []
    for model in models_ct:
        volunteer_perms += list(perms_for(model).filter(codename__startswith="view_"))
        volunteer_perms += list(perms_for(model).filter(codename__startswith="add_"))
    volunteer_group.permissions.set(volunteer_perms)

    admin_group.save()
    volunteer_group.save()

class FundraisingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fundraising'
    verbose_name = _("Arrecadação")

    def ready(self):
        post_migrate.connect(create_groups, sender=self)