from django.conf.urls import url, include

from .views import OrgView, OrgHomeView, AddUserAskView, OrgDetailCourseView, OrgDetailDescView, OrgDetailTeacherView, AddFavView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^userask/$', AddUserAskView.as_view(), name='user_ask'),
    url(r'^orgcourse/(?P<org_id>\d+)/$', OrgDetailCourseView.as_view(), name='org_detail_course'),
    url(r'^orgdesc/(?P<org_id>\d+)/$', OrgDetailDescView.as_view(), name='org_detail_desc'),
    url(r'^orgteacher/(?P<org_id>\d+)/$', OrgDetailTeacherView.as_view(), name='org_detail_teacher'),
    url(r'^addfav/$', AddFavView.as_view(), name='add_fav'),
]
