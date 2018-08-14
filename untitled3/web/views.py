# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from .models import Test, Host
# Create your views here.


def test(request):
    msg = Test.objects.get()
    print(msg[0].conn)
    return HttpResponse(msg)


def addProduct(request):
    name, connList = {"MA20180613": ["123456", "234567", "456789"]}
    conn = Test.objects.all()
    conn.update_or_create(name=name)
