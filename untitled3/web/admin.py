# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from web_1.models import Host, Test


class HostAdmin(admin.ModelAdmin):
    list_display = [
        'hostName',
        'productName',
        'productSn'
    ]

class TestAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


admin.site.register(Host, HostAdmin)
admin.site.register(Test, TestAdmin)