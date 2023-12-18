from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig
from .models import User

@receiver(post_save, sender=User)
def link_employer_to_oversight(sender, instance, created, **kwargs):
    if instance.role == 'oversight' and created:
        employers_to_link = User.objects.filter(oversight_value=instance.email, role='employer')
        for employer in employers_to_link:
            employer.employer = instance
            employer.save()