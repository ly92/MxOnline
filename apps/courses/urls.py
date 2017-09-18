
from django.conf.urls import url, include

from .views import CourseDetailView


urlpatterns = [
    url(r'^coursedetail/$', CourseDetailView.as_view(), name='course_detail'),

]