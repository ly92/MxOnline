__author__ = 'ly'
__date__ = '2017/9/16 下午11:19'

from django import forms

from operation.models import UserAsk

class UserAskForms(forms.ModelForm):
    mobile = forms.CharField(required=True, max_length=11, min_length=11)
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']