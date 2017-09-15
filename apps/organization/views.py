from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页
from .models import CourseOrg, CityDict, Teacher
from users.models import UserProfile
from operation.models import UserFavorite
from courses.models import Course


# Create your views here.


class OrgView(View):
    """
       课程机构列表功能
    """

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # import random
        # for i in range(30,100):
        #     org = CourseOrg()
        #     org.name = '课程' + '%d' % (i)
        #     org.desc = 'desc' + '%d' % (i)
        #     org.address = 'address' + '%d' % (i)
        #     id =  random.randint(1, 5)
        #     city = CityDict.objects.get(id=id)
        #     org.city = city
        #     items = ['pxjg','gr','gx']
        #     org.category = random.choice(items)
        #     org.fav_nums = random.randint(10, 50)
        #     org.click_nums = random.randint(0, 15)
        #     org.students = random.randint(0,100)
        #     org.course_nums = random.randint(1,20)
        #     org.save()
        # for org in all_orgs:
        # org.students = random.randint(0, 100)
        # org.course_nums = random.randint(1, 20)
        # org.desc = org.desc * 2
        # org.address = org.address[0:20]
        # org.name = '机构' + org.name[2:]
        # org.save()

        # 城市
        all_citys = CityDict.objects.all()

        # 机构搜索（全局导航栏中）
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

            # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

            # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

            # 排序类别
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        sub_all_orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': sub_all_orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'keywords': search_keywords,
        })


class OrgHomeView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        import random
        # add course
        # for course in Course.objects.all():
        #     course.delete()
        # for i in range(50, 150):
        #     course = Course()
        #     course.org = CourseOrg.objects.get(id=random.randint(1, 99))
        #     course.name = '课程' + '%d' % (i)
        #     course.desc = 'descripition' + '%d' % (i)
        #     course.detail = 'detail' + '%d' % (i)
        #     course.degree = random.choice(['cj', 'zj', 'gj'])
        #     course.learn_times = random.randint(10, 100)
        #     course.fav_nums = random.randint(0, 20)
        #     course.click_nums = random.randint(0, 50)
        #     course.save()
        #for teacher in Teacher.objects.all():
        #    teacher.work_position = random.choice(['讲师','主任','院长','教授'])
        #    teacher.save()
        # for i in range(30,100):
        #     teacher = Teacher()
        #     teacher.org = CourseOrg.objects.get(id=random.randint(1,99))
        #     teacher.name = '教师' + '%d'%(i)
        #     teacher.work_years = random.randint(1,10)
        #     teacher.work_company = teacher.org.name
        #     teacher.work_position = teacher.org.address
        #     teacher.points = random.choice(['OC','Swift','Python','PHP'])
        #     teacher.click_nums = random.randint(0,40)
        #     teacher.fav_nums = random.randint(0,20)
        #     teacher.save()
        if org:
            # 点击数量+1
            org.click_nums += 1
            org.save()
            # 是否收藏
            has_fav = False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                    has_fav = True
            # 教师
            teachers = org.teacher_set.all()
            # 课程
            courses = org.course_set.all()
            return render(request, 'org-detail-homepage.html', {
                'course_org': org,
                'has_fav': has_fav,
                'teachers': teachers,
                'courses': courses,
            })
        else:
            return render(request, 'active_fail.html', {'msg': '未找到该机构'})
