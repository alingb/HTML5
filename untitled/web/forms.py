#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/7/9 16:36
# FILE:forms.py


from django import forms

from web_1.models import FaeError


class FaeErrorForm(forms.Form):
    class Meta:
        model = FaeError
        fields = '__all__'
