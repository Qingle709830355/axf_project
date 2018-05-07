import random
import time

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

from index.models import UserModel


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':

        name = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户名密码
        if UserModel.objects.filter(username=name).exists():
            user = UserModel.objects.get(username=name)
            if check_password(password, user.password):
                s = 'qwertyuiopasdfghjlkzxcvbnm1234567890'
                ticket = ''
                for i in range(15):
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK_' + ticket + str(now_time)
                response = HttpResponseRedirect('/axf/home')
                user.u_ticket = ticket
                user.save()
                return response
            else:
                return render(request, 'user/user_login.html', {'message': '用户名密码错误'})
        else:
            return render(request, 'user/user_login.html', {'message': '用户不存在'})


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        img = request.FILES.get('icon')
        UserModel.objects.create(
            username=name,
            password=make_password(password),
            email=email,
            icon=img
        )
        return HttpResponseRedirect('/uauth/login')


def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/uauth/login/')
        response.delete_cookie('ticket')
        return HttpResponseRedirect('/uauth/login/')
