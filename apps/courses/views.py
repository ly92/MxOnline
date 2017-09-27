from django.shortcuts import render

from django.db.models import Q
from django.views.generic import View
from .models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class CourseDetailView(View):
    def get(self,request):
        return render(request, 'course-detail.html')



class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all()

        search_key = request.GET.get('keywords', '')
        sort = request.GET.get('sort','')
        if search_key:
            all_courses = all_courses.filter(Q(name__icontains=search_key) | Q(desc__icontains=search_key) | Q(detail__icontains=search_key))

        if sort:
            if sort == 'hot':
                all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses.order_by('-fav_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 9, request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'courses' : courses,
            'course_num' : all_courses.count(),
            'sort' : sort,
            'keywords' : search_key,
        })