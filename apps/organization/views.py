from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
# Create your views here.


class OrgView(View):
    """
       课程机构列表功能
    """
    def get(self,request):
        #课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_num')[:3]

        #城市
        all_citys = CityDict.objects.all()

        #机构搜索（全局导航栏中）
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        #取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        #排序类别
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()

        #对课程机构进行分页


        return render(request, 'org-list.html',{
            'all_orgs' : all_orgs,
            'all_citys' : all_citys,
            'org_nums' : org_nums,
            'city_id' : city_id,
            'category' : category,
            'hot_orgs' : hot_orgs,
            'sort' : sort
        })