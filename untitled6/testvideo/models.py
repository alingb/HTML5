# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Video(models.Model):
    status_choice = (
        (0, u'下线'),
        (1, u'上线'),
    )
    level_choice = (
        (1, u'初级'),
        (2, u'中级'),
        (3, u'高级'),
    )
    status = models.IntegerField(verbose_name='状态', choices=status_choice, default=1)
    level = models.IntegerField(verbose_name='级别', choices=level_choice, default=1)
    classification = models.ForeignKey('Classification', null=True, blank=True)

    weight = models.IntegerField(verbose_name='权重（按从大到小排列）', default=0)

    title = models.CharField(verbose_name='标题', max_length=32)
    summary = models.CharField(verbose_name='简介', max_length=32)
    img = models.ImageField(verbose_name='图片', upload_to='./static/images/Video/')
    href = models.CharField(verbose_name='视频地址', max_length=256)

    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Video'
        verbose_name_plural = u'视频'

    def __str__(self):
        return self.title


class Direction(models.Model):
    weight = models.IntegerField(verbose_name='权重（按从大到小排列）', default=0)
    name = models.CharField(verbose_name='名称', max_length=32)
    classification = models.ManyToManyField('Classification')

    class Meta:
        db_table = 'Direction'
        verbose_name_plural = u'方向（视频方向）'

    def __str__(self):
        return self.name


class Classification(models.Model):
    weight = models.IntegerField(verbose_name='权重（按从大到小排列）', default=0)
    name = models.CharField(verbose_name='名称', max_length=32)

    class Meta:
        db_table = 'Classification'
        verbose_name_plural = u'分类（视频分类）'

    def __str__(self):
        return self.name