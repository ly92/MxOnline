from django.conf.urls import url, include

from .views import OrgView, OrgHomeView, AddUserAskView, OrgDetailCourseView, OrgDetailDescView, OrgDetailTeacherView, AddFavView, TeachersListView, TeacherDetailView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^user/ask/$', AddUserAskView.as_view(), name='user_ask'),
    url(r'^org/course/(?P<org_id>\d+)/$', OrgDetailCourseView.as_view(), name='org_detail_course'),
    url(r'^org/desc/(?P<org_id>\d+)/$', OrgDetailDescView.as_view(), name='org_detail_desc'),
    url(r'^org/teacher/(?P<org_id>\d+)/$', OrgDetailTeacherView.as_view(), name='org_detail_teacher'),
    url(r'^add/fav/$', AddFavView.as_view(), name='add_fav'),

    url(r'^teacher/list/$', TeachersListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]
