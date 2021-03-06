# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from web.models import *


# Create your views here.


def index(req):
    host = Host.objects.all()
    totalNum = len(host)
    runNum = len(host.filter(stress_test="running"))
    # stopNum = len(Host.objects.filter(Q(stress_test="running") |
    #                                   Q(stress_test__contains="OS off")))
    offNum = len(host.filter(status__contains="erro"))
    return render(req, 'index.html', {'totalNum': totalNum, 'runNum': runNum,
                                             'offNum': offNum})


def serverDetail(req):
    global name, status
    name = req.GET.get("name")
    status = req.GET.get("status")
    return render(req, 'serverdetail.html')


def bios(req):
    return render(req, 'bios.html')


def execute(req):
    return render(req, 'execute.html')


def serverInfo(request):
    host = ''
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    search = request.GET.get("search")
    state = request.GET.get("state")
    sort = request.GET.get("sort")
    sortOrder = request.GET.get("sortOrder")
    if name and status:
        print name, status
        if name == "run":
            host = Host.objects.filter(stress_test=status)
        elif name == "error":
            host = Host.objects.filter(status__contains=status)
    if host:
        if state:
            host = host.filter(stress_test=state)
    else:
        host = Host.objects.all()
    if sort and sortOrder:
        if sortOrder == "asc":
            host = host.order_by("{}".format(sort))
        elif sortOrder == "desc":
            host = host.order_by("-{}".format(sort))
    if search:
        host = host.filter(Q(sn__contains=search) |
                           Q(sn_1__contains=search) |
                           Q(name1__contains=search) |
                           Q(name__contains=search) |
                           Q(family__contains=search) |
                           Q(status__contains=search) |
                           Q(ip__contains=search))
    lenth = len(host)
    if offset and limit:
        offset = int(offset)
        limit = int(limit)
        host = host[offset:offset + limit]
    data = []
    for each in host:
        data.append(model_to_dict(each, fields=['id', 'sn', 'sn_1', 'name', 'name1', 'family',
                                                'status', 'bios', 'bmc', 'ip', 'stress_test']))
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


def control(req):
    state = req.POST.get('state')
    if state == "bios":
        msg = req.POST.get('msg')
        if msg:
            msg = json.loads(msg)
        for each in msg:
            print each['ip']
    elif state == "bmc":
        msg = req.POST.get('msg')
        if msg:
            msg = json.loads(msg)
        for each in msg:
            print each['ip']
    elif state == "fru":
        msg = req.POST.get('msg')
        if msg:
            msg = json.loads(msg)
        for each in msg:
            print each['ip']
    elif state == "run":
        msg = req.POST.get('msg')
        info = req.POST.get('info')
        if info:
            info = json.loads(info)
        if msg:
            msg = json.loads(msg)
            for each in msg:
                for i in info:
                    print each['ip'], i
    return HttpResponse()