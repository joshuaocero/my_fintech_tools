import os
from django.db import models
from mtnmomo.collection import Collection
from my_momo_app.async_tasks import collect_funds


class MomoRequest(models.Model):
    mobile_no = models.CharField(max_length=12, blank=False)
    # Change above to num field
    amount = models.CharField(max_length=200, blank=False)
    external_id = models.CharField(max_length=50, blank=False)
    payee_note = models.TextField(blank=False)
    payee_message = models.TextField(blank=False)
    currency = models.CharField(max_length=10, blank=False)
    transaction_ref = models.TextField()
    request_status = models.CharField(
        max_length=10)  # Change this to enum field

    client = Collection({
        "COLLECTION_USER_ID": os.environ.get("COLLECTION_USER_ID"),
        "COLLECTION_API_SECRET": os.environ.get("COLLECTION_API_SECRET"),
        "COLLECTION_PRIMARY_KEY": os.environ.get("COLLECTION_PRIMARY_KEY")
    })

    @staticmethod
    def collect_funds():
        trans_ref = MomoRequest.client.requestToPay(
            mobile="256772123456",
            amount="600",
            external_id="123456789",
            payee_note="dd",
            payer_message="dd",
            currency="EUR")

        print(trans_ref)

    @staticmethod
    def get_status(transaction_ref):
        status = MomoRequest.client.getTransactionStatus(transaction_ref)
        print(status)

    @staticmethod
    def get_balance():
        resp = MomoRequest.client.getBalance()
        print(resp)
