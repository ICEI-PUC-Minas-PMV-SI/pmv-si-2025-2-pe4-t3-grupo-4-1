from django.db import models
from django.contrib.auth import get_user_model
# from core.models import AuditModel

User = get_user_model()


class VolunteerProfile:
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_profile')
  phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='Telefone')
  is_active = models.BooleanField(default=True)

  def __str__(self) -> str:
    return f"{self.user.get_username()} profile"

