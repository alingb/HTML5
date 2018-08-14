#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/4/27 11:10
# FILE:sqlbackup.py

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ytym.settings")
django.setup()

from web.models import Host, TestHost

def getSqlMsg(Obj):
    obj = Obj.objects.order_by('-stress_test').values()[:100]
    return obj


def sqlDelete(Obj):
    obj = Obj.objects.all()
    obj.delete()
    return True


def addSqlMsg(Obj, msg):
    count = 1
    for m in msg:
        m.update(id=count)
        count += 1
        Obj.objects.create(**m)


if __name__ == '__main__':
    msg = getSqlMsg(Host)
    sqlDelete(TestHost)
    addSqlMsg(TestHost, msg)
