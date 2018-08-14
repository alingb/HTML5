# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Host(models.Model):
    hostName = models.CharField(max_length=255)
    productName = models.CharField(max_length=255)
    productSn = models.CharField(max_length=255)

    def __unicode__(self):
        return self.hostName


class Test(models.Model):
    name = models.CharField(max_length=255)
    conn = models.ManyToManyField(Host)

    def __unicode__(self):
        return self.name
