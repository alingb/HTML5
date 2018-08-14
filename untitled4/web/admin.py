# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


# Register your models here.
from web.models import HostMsg


class HostMsgAdmin(admin.ModelAdmin):
    list_display = [
        "hostname",
        "uptime",
        "cpu_stat",
    ]


admin.site.register(HostMsg, HostMsgAdmin)