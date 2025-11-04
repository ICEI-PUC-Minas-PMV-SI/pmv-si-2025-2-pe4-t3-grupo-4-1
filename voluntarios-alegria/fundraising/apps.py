from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FundraisingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fundraising'
    verbose_name = _("Arrecadação")