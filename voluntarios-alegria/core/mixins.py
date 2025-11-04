from django.contrib.auth.models import Group
from django.conf import settings

GROUP_ADMIN = "Administrators"
GROUP_VOL = "Volunteers"

def ensure_default_groups() -> None:
    Group.objects.get_or_create(name=GROUP_ADMIN)
    Group.objects.get_or_create(name=GROUP_VOL)

def user_is_admin(user) -> bool:
    return user.is_superuser or user.groups.filter(name=GROUP_ADMIN).exists()

def user_is_volunteer(user) -> bool:
    return user.groups.filter(name=GROUP_VOL).exists()
