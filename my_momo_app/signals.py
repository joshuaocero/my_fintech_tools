from django.db.models.signals import post_save
from django.dispatch import receiver

from my_momo_app.models import MomoRequest
from my_momo_app.async_tasks import collect_funds

from pprint import pprint


@receiver(post_save, sender=MomoRequest)
def flag_task(sender, instance, **kwargs):
    collect_funds.delay(instance)
    # instance.my_momo_app.save()
