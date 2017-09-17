__author__ = 'ly'
__date__ = '2017/9/16 下午11:19'

from django.forms import ModelForm
from operation.models import UserAsk

class UserAskForms(ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']