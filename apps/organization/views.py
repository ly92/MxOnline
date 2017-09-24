from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页
from .models import CourseOrg, CityDict, Teacher
from users.models import UserProfile
from operation.models import UserFavorite
from courses.models import Course
from .forms import UserAskForms


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
        # for i in range(1, 100):
        #     org = CourseOrg()
        #     org.name = '课程' + '%d' % (i)
        #     org.desc = 'desc' + '%d' % (i)
        #     org.address = 'address' + '%d' % (i)
        #     id = random.randint(1, 5)
        #     city = CityDict.objects.get(id=id)
        #     org.city = city
        #     items = ['pxjg', 'gr', 'gx']
        #     org.category = random.choice(items)
        #     org.fav_nums = random.randint(10, 50)
        #     org.click_nums = random.randint(0, 15)
        #     org.students = random.randint(0, 100)
        #     org.course_nums = random.randint(1, 20)
        #     org.students = random.randint(0, 100)
        #     org.course_nums = random.randint(1, 20)
        #     org.desc = org.desc * 2
        #     org.address = org.address[0:20]
        #     org.name = '机构' + org.name[2:]
        #     org.save()
        # for org in all_orgs:
        #     org.students = random.randint(0, 100)
        #     org.course_nums = random.randint(1, 20)
        #     org.desc = org.desc * 2
        #     org.address = org.address[0:20]
        #     org.name = '机构' + org.name[2:]
        #     org.save()

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


class AddUserAskView(View):
    """
       用户添加咨询
    """

    def post(self, request):
        user_ask_form = UserAskForms(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)
            return HttpResponse('{"status" : "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status" : "fail", "msg" : "添加出错"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        # import random
        # add course
        # for course in Course.objects.all():
        #     course.delete()
        # for i in range(1, 150):
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
        # for i in range(1, 100):
        #     teacher = Teacher()
        #     teacher.org = CourseOrg.objects.get(id=random.randint(1, 99))
        #     teacher.name = '教师' + '%d' % (i)
        #     teacher.work_years = random.randint(1, 10)
        #     teacher.work_company = teacher.org.name
        #     teacher.work_position = teacher.org.address
        #     teacher.points = random.choice(['OC', 'Swift', 'Python', 'PHP'])
        #     teacher.click_nums = random.randint(0, 40)
        #     teacher.fav_nums = random.randint(0, 20)
        #     teacher.work_position = random.choice(['讲师', '主任', '院长', '教授'])
        #     teacher.save()
        if org:
            current_page = 'home'
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
                'current_page': current_page,
            })
        else:
            return render(request, 'active_fail.html', {'msg': '未找到该机构'})


class OrgDetailCourseView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        if org:
            current_page = 'home'
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
            return render(request, 'org-detail-course.html', {
                'course_org': org,
                'has_fav': has_fav,
                'teachers': teachers,
                'courses': courses,
                'current_page': current_page,
            })
        else:
            return render(request, 'active_fail.html', {'msg': '未找到该机构'})


class OrgDetailDescView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        if org:
            current_page = 'home'
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
            return render(request, 'org-detail-desc.html', {
                'course_org': org,
                'has_fav': has_fav,
                'teachers': teachers,
                'courses': courses,
                'current_page': current_page,
            })
        else:
            return render(request, 'active_fail.html', {'msg': '未找到该机构'})


class OrgDetailTeacherView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=org_id)
        if org:
            current_page = 'home'
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
            return render(request, 'org-detail-teachers.html', {
                'course_org': org,
                'has_fav': has_fav,
                'teachers': teachers,
                'courses': courses,
                'current_page': current_page,
            })
        else:
            return render(request, 'active_fail.html', {'msg': '未找到该机构'})


class AddFavView(View):
    """
    收藏／取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id')
        fav_type = request.POST.get('fav_type')  # (1,"课程"),(2,"课程机构"),(3,"教师")
        if request.user.is_authenticated:
            favs = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if favs:
                for fav in favs:
                    if fav_type == 1:
                        course = Course.objects.get(id=int(fav_id))
                        if course.fav_nums > 0:
                            course.fav_nums -= 1
                            course.save()
                    elif fav_type == 2:
                        courseOrg = CourseOrg.objects.get(id=int(fav_id))
                        if courseOrg.fav_nums > 0:
                            courseOrg.fav_nums -= 1
                            courseOrg.save()
                    else:
                        teacher = Teacher.objects.get(id=int(fav_id))
                        if teacher.fav_nums > 0:
                            teacher.fav_nums -= 1
                            teacher.save()
                    fav.delete()
                return HttpResponse('{"status" : "success", "msg" : "收藏"}', content_type='application/json')
            else:
                fav = UserFavorite()
                fav.fav_type = fav_type
                fav.fav_id = fav_id
                fav.user = request.user
                fav.save()
                if fav_type == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:
                    courseOrg = CourseOrg.objects.get(id=int(fav_id))
                    courseOrg.fav_nums += 1
                    courseOrg.save()
                else:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
        else:
            return HttpResponse('{"status" : "fail", "msg" : "用户未登录"}', content_type='application/json')
