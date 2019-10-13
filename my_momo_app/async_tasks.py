import os
import json
from mtnmomo.collection import Collection
from celery.decorators import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task(name="collect_funds")
def collect_funds(request):
    """sends an request to collect funds from the payer"""
    client = Collection({
        "COLLECTION_USER_ID": os.environ.get("COLLECTION_USER_ID"),
        "COLLECTION_API_SECRET": os.environ.get("COLLECTION_API_SECRET"),
        "COLLECTION_PRIMARY_KEY": os.environ.get("COLLECTION_PRIMARY_KEY")
    })

    response = client.requestToPay(
        mobile=request.mobile_no,
        amount=request.amount,
        external_id=request.external_id,
        payee_note=request.payee_note,
        payer_message=request.payee_message,
        currency=request.currency)

    from my_momo_app.models import MomoRequest
    momo_request = MomoRequest.objects.filter(id=request.id)
    if 'transaction_ref' in response:
        momo_request.update(request_status="complete",
                            transaction_ref=response['transaction_ref'])
    momo_request.update(lastest_api_response=response)
