#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django import forms
from django.forms import ModelForm
from django.forms import CharField
from django.forms import Textarea


class ArticleForm(ModelForm):
    abstract = CharField(label='文章摘要',
                         widget=Textarea(attrs={'cols': 100, 'rows': 7}),
                         required=False)

    # # 隐藏字段 
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)