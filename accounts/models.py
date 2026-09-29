from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("CUSTOMER", "Customer"),
        ("OWNER", "Restaurant Owner"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CUSTOMER")

    def __str__(self):
        return f"{self.user.username} ({self.role})"

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)