from __future__ import absolute_import

import os
from django.conf import settings
from celery import Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from mtnmomo.collection import Collection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_fintech_tools.settings')
app = Celery('my_fintech_tools')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@task(name="collect_funds")
def collect_funds(r_id, mobile_no, amount, external_id, payee_note, payee_message, currency):
    """
    Sends an request to collect funds from the payer
    """
    client = Collection({
        "COLLECTION_USER_ID": os.environ.get("COLLECTION_USER_ID"),
        "COLLECTION_API_SECRET": os.environ.get("COLLECTION_API_SECRET"),
        "COLLECTION_PRIMARY_KEY": os.environ.get("COLLECTION_PRIMARY_KEY")
    })

    response = client.requestToPay(
        mobile=mobile_no,
        amount=amount,
        external_id=external_id,
        payee_note=payee_note,
        payer_message=payee_message,
        currency=currency)

    # We'll do the import here as celery is loaded before Django apps
    from my_momo_app.models import MomoRequest
    momo_request = MomoRequest.objects.filter(id=r_id)
    if 'transaction_ref' in response:
        momo_request.update(request_status="PENDING",
                            transaction_ref=response['transaction_ref'])
    momo_request.update(lastest_api_response=response)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="check_transaction_status",
    ignore_result=True
)
def check_transaction_status():
    """
    Checks the status of a transaction
    """
    client = Collection({
        "COLLECTION_USER_ID": os.environ.get("COLLECTION_USER_ID"),
        "COLLECTION_API_SECRET": os.environ.get("COLLECTION_API_SECRET"),
        "COLLECTION_PRIMARY_KEY": os.environ.get("COLLECTION_PRIMARY_KEY")
    })

    # We'll do the import here as celery is loaded before Django apps
    from my_momo_app.models import MomoRequest
    momo_requests = MomoRequest.objects.filter(request_status='PENDING')

    for momo_request in momo_requests:
        response = client.getTransactionStatus(momo_request.transaction_ref)
        if 'status' in response:
            mk = MomoRequest.objects.filter(id=momo_request.id)
            mk.update(
                request_status=response['status'], lastest_api_response=response)
