# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class HostMsg(models.Model):
    hostname = models.CharField("hostname", max_length=255, blank=True)
    uptime = models.CharField("uptime", max_length=255, unique=True)
    cpu_stat = models.CharField("cpu_stat", max_length=50)
    date_time = models.DateTimeField()


