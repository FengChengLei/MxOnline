from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import redis

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm
from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile
# Create your views here.


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            'login_form': login_form
        })

    def post(self, request, *args, **kwargs):
        # user_name = request.POST.get('username', '')
        # password = request.POST.get('password', '')
        # if not user_name:
        #     return render(request, 'login.html',{'msg': '请输入用户名'})
        # if not password:
        #     return render(request,'login.html', {'msg': '请输入密码'})
        # if len(password) < 3:
        #     return render(request, 'login.html', {'msg': '密码格式不正确'})

        # 表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 通过用户和密码查询用户是否存在
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # 查询到用户后，进行登录认证
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            # 验证码正确，发送手机验证码
            mobile = send_sms_form.cleaned_data['mobile']
            # 随机生成数字验证码
            code = generate_random(4,0)
            re_json = send_single_sms(yp_apikey, code, mobile)
            if re_json['code'] == 0:
                re_dict['status'] = 'success'
                r = redis.Redis(REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 300) # 设置验证码5分钟过期
            else:
                re_dict['msg'] = re_json['msg']
        else:
            for key, error in send_sms_form.errors.items():
                re_dict[key] = error[0]

        return JsonResponse(re_dict)


class DynamicLoginView(View):
    def post(self,request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = login_form.cleaned_data['mobile']
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                # 新建用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            d_form = DynamicLoginForm()
            return render(request, 'login.html', {'login_form': login_form, 'dynamic_login': dynamic_login, 'd_form': d_form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, 'register.html', {'register_get_form': register_get_form})

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = register_post_form.cleaned_data['mobile']
            password = register_post_form.cleaned_data['password']

            # 新建用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            register_get_form = RegisterGetForm()
            return render(request, 'register.html', {
                'register_get_form': register_get_form,
                'register_post_form': register_post_form
            })
