
from django.conf.urls import url, include


from .views import OrgView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),

]