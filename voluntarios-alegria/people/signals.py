from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import VolunteerProfile
from core.mixins import ensure_default_groups, GROUP_VOL

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile_and_default_group(sender, instance, created, **_):
  if created:
    VolunteerProfile.objects.get_or_create(user=instance, defaults={"created_by": instance})
    ensure_default_groups()