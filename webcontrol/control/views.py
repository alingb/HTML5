# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from web.models import *
# Create your views here.


def index(req):
    return render(req, 'index.html')


def serverDetail(req):
    return render(req, 'serverdetail.html')


def bios(req):
    return render(req, 'bios.html')


def ipmi(req):
    return render(req, 'ipmi.html')


def serverInfo(request):
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    search = request.GET.get("search")
    state = request.GET.get("state")
    if state:
        host = Host.objects.filter(stress_test=state)
    else:
        host = Host.objects.all()
    host = host.order_by('-id')
    lenth = len(host)
    if not offset or not limit:
        host = host
    else:
        offset = int(offset)
        limit = int(limit)
        host = host[offset:offset + limit]
    data = []
    for each in host:
        data.append(model_to_dict(each, fields=['id', 'sn', 'sn_1', 'name', 'name1', 'family',
                                               'status', 'bios', 'bmc', 'stress_test']))
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))

