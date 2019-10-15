import os
from django.db import models


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
    lastest_api_response = models.TextField()
