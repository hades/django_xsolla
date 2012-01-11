from django.contrib import admin

from django_xsolla.models import *

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['rcvd_at', 'v1', 'summ']

admin.site.register(Transaction, TransactionAdmin)
