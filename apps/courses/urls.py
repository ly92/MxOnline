from django.conf.urls import url, include

from .views import CourseDetailView, CourseListView

urlpatterns = [
    url(r'^coursedetail/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^courselist/$', CourseListView.as_view(), name='course_list'),
]
