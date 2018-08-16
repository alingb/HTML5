# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from web_1.models import HostMsg


def index(request):
    msg = HostMsg.objects.all()
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return render(request, os.path.join(PROJECT_ROOT, '../../untitled/templates', "index.html"), {"msg": msg})


def product(request):
    msg = {"name": "MA01020304"}
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return render(request, os.path.join(PROJECT_ROOT, '../../untitled/templates', "product.html"), {"msg": msg})


def producrDetail(request):
    msg = {"name": "MA01020304"}
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return render(request, os.path.join(PROJECT_ROOT, '../../untitled/templates', "product_detail.html"), {"msg": msg})