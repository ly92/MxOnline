from django.conf.urls import url, include

from .views import OrgView, OrgHomeView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
]
