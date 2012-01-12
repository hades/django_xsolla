from django.db import models
from django.utils.translation import ugettext_lazy as _

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

    def __unicode__(self):
        return u"xsolla transfer by {0} id {1}".format(self.v1, self.ident)

    class Meta:
        get_latest_by = 'rcvd_at'
        ordering = ('-rcvd_at',)
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
