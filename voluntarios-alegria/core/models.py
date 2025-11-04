from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_%(class)s_set', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Criado por"))

    class Meta:
        abstract = True
