# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from web_1.forms import FaeErrorForm
from web_1.models import FaeError



def test(req):
    EXCLUSION = {'1': '处理中',
                 '2': '已完成'}
    CUSTOMER = {'1': '锐捷',
                '2': '深信服',
                '3': '三盟', }
    PRODUCT = {
        'ASR1100': '华硕ASR1100',
        'K880G3': '英业达K880G3',
        'ASD2550': '华硕ASD2550',
        'RS720Q-E8': '华硕RS720Q-E8',
        'RS300-E9-PS4': '华硕RS300-E9-PS4',
        'ASR2612': '华硕ASR2612',
        'D51B-2U': '广达D51B-2U',
        'T41S-2U': '广达T41S-2U',
        'RS300-E9-PS4': '华硕RS300-E9-PS4',
        'RS520-E8-RS8': '华硕RS520-E8-RS8',
        'S210-X22RQ': '广达S210-X22RQ',
        'ESC4000G3': '华硕ESC4000G3',
        'RS520-E8-RS12': '华硕RS520-E8-RS12', }
    USER = {'daipeibin': u'戴沛斌',
            'huangjiaqi': u'黄嘉琪',
            'jinanning': u'金安宁',
            'laiwenlong': u'赖文龙',
            'lichao': u'李超',
            'liming': u'李铭',
            'maimaotao': u'麦茂涛',
            'wangqiang': u'王强',
            'xieliye': u'谢立业',
            'zhengcongke': u'郑淙珂',
            'zhongyangchun': u'仲扬春',
            'linliubin': u'林柳彬',
            'lingbing': u'凌兵', }
    if not req.user.username:
        return HttpResponseRedirect('/login/')
    user = req.user.username
    username = req.session.get('username', '')
    number = random.randint(100000, 999999)
    try:
        num_exist = FaeError.objects.get(num=number).num
    except:
        num_exist = ''
    while number == num_exist:
        number = random.randint(100000, 999999)
    if req.POST:
        form = FaeErrorForm(req.POST, req.FILES)
        if form.is_valid():
            error = FaeError()
            customer = form.cleaned_data['customer_name']
            product = form.cleaned_data['product_name']
            if customer == 'other':
                error.customer = form.cleaned_data['customer_name_other']
            else:
                error.customer = CUSTOMER[customer]
            if product == 'other':
                error.product = form.cleaned_data['product_name_other']
            else:
                error.product = PRODUCT[product]
            if form.cleaned_data['customer_name_other']:
                error.customer_name_other = form.cleaned_data['customer_name_other']
            if form.cleaned_data['product_name_other']:
                error.product_name_other = form.cleaned_data['product_name_other']
            error.num = form.cleaned_data['num']
            error.product_name = form.cleaned_data['product_name']
            error.customer_name = form.cleaned_data['customer_name']
            error.exclusion_phase = form.cleaned_data['exclusion_phase']
            error.exclusion = EXCLUSION[form.cleaned_data['exclusion_phase']]
            error.sn = form.cleaned_data['sn']
            error.enclosure = form.cleaned_data['enclosure']
            error.phenomenon_description = form.cleaned_data['phenomenon_description']
            error.configuration_information = form.cleaned_data['configuration_information']
            error.resolvent = form.cleaned_data['test_model']

            if username:
                try:
                    error.user = USER[username]
                except:
                    error.user = username
            else:
                try:
                    error.user = USER[user]
                except:
                    error.user = user
            if form.cleaned_data['exclusion_phase'] == '2':
                error.status = True
            list_phenomenon_description = ''
            list_configuration_information = ''
            if "\r\n" in error.phenomenon_description:
                for i in error.phenomenon_description.split('\r\n'):
                    list_phenomenon_description += i + '\r\n\t\t\t    '
                error.phenomenon_description = list_phenomenon_description.strip()
            if "\r\n" in error.configuration_information:
                for i in error.configuration_information.split('\r\n'):
                    list_configuration_information += i + '\r\n\t\t'
                error.configuration_information = list_configuration_information.strip()
            information = u'''问题描述:%s
    %s
    软件和硬件配置信息:%s
    %s
    解决方法::%s''' % (
            error.phenomenon_description, '=' * 20, error.configuration_information, '=' * 20, error.resolvent)
            error.bug_record = information
            error.save()
            data = FaeError.objects.all()
            total_num = data.count()
            for i in data:
                i.number = total_num
                total_num -= 1
                i.save()
            return HttpResponseRedirect('/technology/technology/error/')
    else:
        form = FaeErrorForm()
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return render(req, os.path.join(PROJECT_ROOT, 'technology/templates', 'fae_erro.html'),
                  {'form': form, 'num': number, 'user': user})

