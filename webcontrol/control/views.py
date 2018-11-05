# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


def index(req):
    return render(req, 'index.html')


def serverDetail(req):
    return render(req, 'serverdetail.html')


def bios(req):
    return render(req, 'bios.html')


def ipmi(req):
    return render(req, 'ipmi.html')