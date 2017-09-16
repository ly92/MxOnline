# _*_ coding: utf-8 _*_
__author__ = 'ly'
__date__ = '2017/9/16 下午11:19'

from django import forms
from operation.models import UserAsk

class UserAskForms(forms.ModelForm):
    class Meta:
        models = UserAsk
        fields = ['name', 'mobile', 'course_name']