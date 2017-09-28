from django.shortcuts import render

from django.db.models import Q
from django.views.generic import View
from .models import Course, Lesson
from operation.models import UserCourse
from organization.models import Teacher

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from django.http import HttpResponse



class CourseDetailView(View):
    def get(self,request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        users = UserCourse.objects.filter(course=course)

        org_teachers = Teacher.objects.filter(org=course.org)
        org_courses = Course.objects.filter(org=course.org)

        lessons = Lesson.objects.filter(course=course)
        return render(request, 'course-detail.html',
                      {'course' : course,
                       'users' : users,
                       'lessons' : lessons,
                       'org_teachers' : org_teachers,
                       'org_courses' : org_courses,
                       })



class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by('-click_nums')[:3]
        search_key = request.GET.get('keywords', '')
        sort = request.GET.get('sort','')
        if search_key:
            all_courses = all_courses.filter(Q(name__icontains=search_key) | Q(desc__icontains=search_key) | Q(detail__icontains=search_key))

        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses = all_courses.order_by('-fav_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 9, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            'courses' : courses,
            'course_num' : all_courses.count(),
            'sort' : sort,
            'keywords' : search_key,
            'hot_courses' : hot_courses,
        })