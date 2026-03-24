from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Collect


@receiver(post_delete, sender=Collect)
def delete_cover(sender, instance, **kwargs):
    if instance.cover:
        instance.cover.delete(save=False)