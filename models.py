from django.db import models

class Transaction(models.Model):
    v1 = models.CharField(max_length=32)
    v2 = models.CharField(max_length=32, blank=True)
    v3 = models.CharField(max_length=32, blank=True)
    summ = models.DecimalField(max_digits=12, decimal_places=3)
    sent_at = models.DateTimeField()
    rcvd_at = models.DateTimeField(auto_now_add=True)
    test = models.BooleanField()
    bonus = models.CharField(max_length=32)
    ident = models.CharField(max_length=32)
