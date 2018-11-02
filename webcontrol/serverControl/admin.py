# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from serverControl.models import ServerMsg

admin.site.register(ServerMsg)
