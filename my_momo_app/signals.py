from django.db.models.signals import post_save
from django.dispatch import receiver

from my_momo_app.models import MomoRequest
from my_fintech_tools.celery import collect_funds


@receiver(post_save, sender=MomoRequest)
def flag_collection_task(sender, instance, **kwargs):
	"""
	After a model save event, make an API request to
	the MoMo API
	"""
    collect_funds.delay(instance.id, instance.mobile_no, instance.amount,
                        instance.external_id, instance.payee_note, instance.payee_message, instance.currency)
