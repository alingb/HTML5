#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/4/27 11:10
# FILE:sqlbackup.py

import django
import os
from web_1.models import Host, TestHost


def getSqlMsg(Obj):
    obj = Obj.objects.order_by('-stress_test').values()[:100]
    msg, count = {}, 1
    for ht in obj:
        ht.update(id=count)
        msg.update(ht)
    return msg


def sqlDelete(Obj):
    obj = Obj.objects.all()
    obj.delete()
    return True


def addSqlMsg(Obj, msg):
    for m in msg:
        Obj.objects.create(**m)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ytym.settings")
    django.setup()
    msg = getSqlMsg(Host)
    sqlDelete(TestHost)
    addSqlMsg(TestHost, msg)
