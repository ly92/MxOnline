from django.shortcuts import render

from django.views.generic import View

# Create your views here.

class CourseDetailView(View):
    def get(self,request):
        return render(request, 'course-detail.html')