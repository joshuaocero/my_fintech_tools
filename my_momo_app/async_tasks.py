import os
from my_momo_app.models import MomoRequest
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

    trans_ref = client.requestToPay(
        mobile=request.mobile_no,
        amount=request.amount,
        external_id=request.external_id,
        payee_note=request.payee_note,
        payer_message=request.payee_message,
        currency=request.currency)

    if trans_ref['transaction_ref']:
        momo_request = MomoRequest.objects.get(id=request.id)
        momo_request.transaction_ref = trans_ref['transaction_ref']
