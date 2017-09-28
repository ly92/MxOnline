from django.conf.urls import url, include

from .views import CourseDetailView, CourseListView

urlpatterns = [
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
]
