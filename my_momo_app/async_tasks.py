import os
import json
from mtnmomo.collection import Collection
from celery.decorators import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task(name="collect_funds")
def collect_funds(r_id, mobile_no, amount, external_id, payee_note, payee_message, currency):
    """sends an request to collect funds from the payer"""
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

    from my_momo_app.models import MomoRequest
    momo_request = MomoRequest.objects.filter(id=r_id)
    if 'transaction_ref' in response:
        momo_request.update(request_status="pending",
                            transaction_ref=response['transaction_ref'])
    momo_request.update(lastest_api_response=response)
