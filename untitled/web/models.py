# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
BUG_CHOICES = (
    ('1', '一般'),
    ('2', '严重'),
    ('3', '非常严重'),
)
PRODUCT_CHOICES = (
    ('ASR1100', '华硕ASR1100'),
    ('K880G3', '英业达K880G3'),
    ('ASD2550', '华硕ASD2550'),
    ('RS720Q-E8', '华硕RS720Q-E8'),
    ('RS300-E9-PS4', '华硕RS300-E9-PS4'),
    ('ASR2612', '华硕ASR2612'),
    ('D51B-2U', '广达D51B-2U'),
    ('T41S-2U', '广达T41S-2U'),
    ('RS300-E9-PS4', '华硕RS300-E9-PS4'),
    ('RS520-E8-RS8', '华硕RS520-E8-RS8'),
    ('S210-X22RQ', '广达S210-X22RQ'),
    ('ESC4000G3', '华硕ESC4000G3'),
    ('RS520-E8-RS12', '华硕RS520-E8-RS12'),
    ('other', '其他'),
)
PROJECT_CHOICES = (
    ('ELOG', '锐捷ELOG'),
    ('RG-RCP', '锐捷RG-RCP'),
    ('RCD6000-Office', '锐捷RCD6000-Office'),
    ('RCD6000-Main', '锐捷RCD6000-Main'),
    ('RG-SE04', '锐捷RG-SE04'),
    ('RG-ONC-AIO-CTL', '锐捷RG-ONC-AIO-CTL'),
    ('RG-RCM1000-Office', '锐捷RG-RCM1000-Office'),
    ('RG-RCM1000-Edu', '锐捷RG-RCM1000-Edu'),
    ('RG-RCM1000-Smart', '锐捷RG-RCM1000-Smart'),
    ('MDBE', '美电贝尔'),
    ('ZJCC', '广东紫晶存储'),
    ('UDS1022-G', '锐捷UDS1022-G'),
    ('UDS1022-G1', '锐捷UDS1022-G1'),
    ('UDS2000-C', '锐捷UDS2000-C'),
    ('UDS2000-E', '锐捷UDS2000-E'),
    ('UDS2000-E1', '锐捷UDS2000-E1'),
    ('RG-CES', '锐捷RG-CES'),
    ('RG-CPV-M', '锐捷RG-CPV-M'),
    ('RG-CPV-S', '锐捷RG-CPV-S'),
    ('2513(M1)', '三盟2513(M1)'),
    ('2513(M3)', '三盟2513(M3)'),
    ('2513(VM3)', '三盟2513(VM3)'),
    ('ASERVER-2400', '深信服ASERVER-2400'),
    ('ASERVER-2405', '深信服ASERVER-2405'),
    ('VDS-5050', '深信服VDS-5050'),
    ('VDS-6550', '深信服VDS-6550'),
    ('VDS-8050', '深信服VDS-8050'),
    ('VDS-G680', '深信服VDS-G680'),
    ('other', '其他'),
)
EXCLUSION_CHOICES = (
    ('1', '处理中'),
    ('2', '已完成'),
)
CUSTOMER_CHOICES = (
    ('1', '锐捷'),
    ('2', '深信服'),
    ('3', '三盟'),
    ('other', '其他'),

)
DISCOVERY_CHOICES = (
    ('1', '公司内部'),
    ('2', '客户'),
    ('other', '其他')
)


class FaeError(models.Model):
    num = models.IntegerField('bug编号', blank=True)

    product_name = models.CharField('产品名称', choices=PRODUCT_CHOICES, max_length=500)
    product_name_other = models.CharField('其他产品名称', max_length=500, blank=True, )
    customer_name = models.CharField('客户名称', choices=CUSTOMER_CHOICES, max_length=500)
    customer_name_other = models.CharField('其他客户名称', max_length=500, blank=True)
    customer = models.CharField('客户名称', max_length=500, blank=True)
    exclusion_phase = models.CharField('处理阶段', choices=EXCLUSION_CHOICES, max_length=500)
    exclusion = models.CharField('处理阶段', max_length=500, blank=True)
    sn = models.CharField('产品sn', max_length=250)
    enclosure = models.FileField('附件上传', blank=True)
    phenomenon_description = models.CharField('bug现象详细描述', max_length=500)
    configuration_information = models.CharField('配置信息', max_length=500)
    resolvent = models.CharField('解决方法', max_length=500)
    bug_record = models.TextField('BUG记录', blank=True)
    submission_time = models.DateTimeField('提交时间', auto_now_add=True)
    record_time = models.DateTimeField('更新时间', auto_now=True)
    time = models.CharField('更新时间', max_length=250, blank=True, )
    user = models.CharField('修改者', max_length=50, blank=True, )
    status = models.BooleanField(default=False)
    number = models.CharField('编号', max_length=50, blank=True)

    class Meta:
        verbose_name = u'fault'
        verbose_name_plural = u'bugsystem'
