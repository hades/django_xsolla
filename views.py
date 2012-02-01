import hashlib

from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.utils.html import escape

from django.contrib.auth.models import User

from django_xsolla.models import *

try:
    SECRET_KEY = settings.DJANGO_XSOLLA_SECRET_KEY
except AttributeError, e:
    raise ImproperlyConfigured, "Some settings are missing: {0}".format(e.message)

class XmlResponse(HttpResponse):
    def __init__(self, data):
        xml = u"""<?xml version="1.0" encoding="windows-1251"?>
<response>
 {0}
</response>""".format("\n".join([ "<{0}>{1}</{0}>".format(k, escape(data[k]))
                                  for k in data ]))
        super(XmlResponse, self).__init__(content=xml.encode('cp1251'),
                                          mimetype="application/xml")

def xsolla_request(func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            output = {'result': 7,
                      'comment': 'I accept only GET requests'}
        else:
            output = func(request, *args, **kwargs)
        response = XmlResponse(output)
        return response
    wrapper.__name__ = func.__name__
    wrapper.__module__ = func.__module__
    wrapper.__doc__ = func.__doc__
    return wrapper

def check_md5(md5, *args):
    return md5.lower() == hashlib.md5(''.join(args)).hexdigest().lower()

@xsolla_request
def payment(request):
    command = request.GET.get('command', '')
    try:
        if command == 'check':
            v1 = request.GET['v1']
            md5 = request.GET['md5']
            if not check_md5(md5, command, v1, SECRET_KEY):
                return {'result': 3, 'comment': 'invalid signature'}
            if User.objects.filter(pk=v1).exists():
                return {'result': 0}
            else:
                return {'result': 7, 'comment': 'user does not exist'}
        elif command == 'pay':
            v1 = request.GET['v1']
            v2 = request.GET.get('v2', '')
            v3 = request.GET.get('v3', '')
            i = request.GET['id']
            summ = Decimal(request.GET['sum']).quantize(Decimal("1.00"))
            date = request.GET['date']
            test = int(request.GET.get('test', 0))
            bonus = request.GET.get('bonus', '')
            md5 = request.GET['md5']

            try:
                date = datetime.strptime(date, '%Y%m%d%H%M%S')
            except ValueError, e:
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            if not check_md5(md5, command, v1, i, SECRET_KEY):
                return {'result': 3, 'comment': 'invalid signature'}
            t, created = Transaction.objects.get_or_create(ident=i,
                                                           defaults={'v1': v1,
                                                                     'v2': v2,
                                                                     'v3': v3,
                                                                     'summ': summ,
                                                                     'sent_at': date,
                                                                     'test': test,
                                                                     'bonus': bonus,
                                                           })
            return {'result': 0, 'id': t.ident, 'id_shop': t.pk, 'sum': t.summ}
        else:
            return {'result': 4,
                    'comment': 'unknown command {0}'.format(command)}
    except KeyError, e:
        return {'result': 4,
                'comment': e.message}
