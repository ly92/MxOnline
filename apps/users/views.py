from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from users.models import UserProfile
from .forms import LoginForm

# Create your views here.

# login in class
class LoginView(View):
    def get(self,request):
        return render(request, 'login.html',{})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg' : '用户未激活'})
            else:
                return render(request, 'login.html', {'msg' : '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form' : login_form})
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



