from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from users.models import UserProfile, EmailVerifyRecord
from operation.models import UserMessage
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_email
from datetime import datetime


# Create your views here.

# login in class 登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# # login in method
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username','')
#         password = request.POST.get('password','')
#
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request,user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html',{'msg':'用户名或者密码错误'})
#     elif request.method == 'GET':
#         return render(request,'login.html',{})

# 退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html')


# 注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):  # 判断用户是否存在
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            password = request.POST.get('password', '')
            user = UserProfile()
            user.email = email
            user.username = email
            user.password = make_password(password)
            user.is_active = False  # 数据库中is_active 默认是False 没有激活,当变为True时为激活
            user.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user.id
            user_message.message = '欢迎注册'
            user_message.save()

            send_email(email, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_recodes = EmailVerifyRecord.objects.filter(code=active_code)
        if all_recodes:
            for recode in all_recodes:
                dis = datetime.now() - recode.send_time
                if recode.is_usable and dis.seconds < 10 * 60:
                    recode.is_usable = False
                    recode.save()
                    email = recode.email
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                else:
                    return render(request, 'active_fail.html', {'msg' : '激活失败！'})
        else:
            return render(request, 'active_fail.html', {'msg' : '激活失败！'})
        return render(request, 'login.html')


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPasswordForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPasswordForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                user = UserProfile.objects.get(email=email)
                if user is not None:
                    send_email(email, 'forget')
                return render(request, 'success.html')
            else:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form , 'msg': '用户不存在'})
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码
class ResetPwdView(View):
    def get(self, request, reset_code):
        all_recodes = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_recodes:
            for recode in all_recodes:
                dis = datetime.now() - recode.send_time
                if recode.is_usable and dis.seconds < 10 * 60:
                    email = recode.email
                    recode.is_usable = False
                    recode.save()
                    return render(request, 'password_reset.html', {'email' : email})
                else:
                    return render(request, 'active_fail.html', {'msg': '验证码已失效'})
        else:
            return render(request, 'active_fail.html', {'msg': '验证码已失效'})
        return render(request, 'login.html')
            # return render(request, 'password_reset.html', {'msg' : '验证码已失效'})


# 修改并记录密码到数据库
class ModifyPwdView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '两次输入的密码不一致', 'email': email})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd1)
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'modify_form' : modify_form, 'email' : email})