import os

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm, UploadImageForm, UserInfoForm, ChangePwdForm, UpdateMobileForm
from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT, BASE_DIR
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile
from apps.operations.models import UserCourse, UserFavourite, UserMessage,Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course

# Create your views here.


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        banners = Banner.objects.all()[:3]
        next = request.GET.get('next', '')
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            'login_form': login_form,
            'next': next,
            'banners': banners,
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
        banners = Banner.objects.all()[:3]

        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 通过用户和密码查询用户是否存在
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # 查询到用户后，进行登录认证
                login(request, user)
                # 登录成功之后应该返回页面
                next = request.GET.get('next', '')
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'login.html', {
                    'msg': '用户名或密码错误',
                    'banners': banners,
                })
        else:
            return render(request, 'login.html', {
                'login_form': login_form,
                'banners': banners,
            })


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            # 验证码正确，发送手机验证码
            mobile = send_sms_form.cleaned_data['mobile']
            # 随机生成数字验证码
            code = generate_random(4, 0)
            re_json = send_single_sms(yp_apikey, code, mobile)
            if re_json['code'] == 0:
                re_dict['status'] = 'success'
                r = redis.Redis(REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 300) # 设置验证码5分钟过期
            else:
                re_dict['status'] = 'fail'
                re_dict['msg'] = re_json['msg']
        else:
            for key, error in send_sms_form.errors.items():
                re_dict[key] = error[0]
        print(re_dict.get('msg', '无'))
        return JsonResponse(re_dict)


class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        banners = Banner.objects.all()[:3]
        next = request.GET.get('next', '')
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            'login_form': login_form,
            'next': next,
            'banners': banners,
        })

    def post(self,request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        banners = Banner.objects.all()[:3]
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
            return render(request, 'login.html', {'login_form': login_form, 'dynamic_login': dynamic_login, 'd_form': d_form, 'banners':banners})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all()[:3]
        register_get_form = RegisterGetForm()
        return render(request, 'register.html', {'register_get_form': register_get_form, 'banners':banners})

    def post(self, request, *args, **kwargs):
        banners = Banner.objects.all()[:3]
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
                'register_post_form': register_post_form,
                'banners':banners
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, *args, **kwargs):
        captcha_form = RegisterGetForm()
        current_page = 'info'
        return render(request,'usercenter-info.html', {
            'captcha_form': captcha_form,
            'current_page': current_page,
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse(user_info_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login'
    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                'status': 'success'
            })
        return JsonResponse({
            'status': 'fail'
        })
    #     files = request.FILES['image']
    #     self.save_file(files)
    #
    # def save_file(self, file):
    #     with open(os.path.join(BASE_DIR, 'media/head_image/uploaded.jpg'),'wb')as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)


class ChangePwdView(View):
    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = pwd_form.cleaned_data['password1']
            # pwd2 = pwd_form.cleaned_data['password2']
            #
            # if pwd1 !=pwd2:
            #     return JsonResponse({
            #         'status': 'fail',
            #         'msg': '密码不一致'
            #     })
            user = request.user
            user.set_password(pwd1)
            user.save()
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse(pwd_form.errors)


class ChangeMobileView(LoginRequiredMixin, View):
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data['mobile']
            # 已经存在的记录不能重复注册
            if request.user.mobile == mobile:
                return JsonResponse({
                    'mobile':'和当前号码一致'
                })

            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    'mobile': '该手机号已经被占用'
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile
            user.save()
            return JsonResponse({
                'status':'success'
            })
        else:
            return JsonResponse(mobile_form.errors)


class MyCourseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        my_courses = UserCourse.objects.filter(user=request.user)

        current_page = 'mycourse'
        return render(request, 'usercenter-mycourse.html', {
            'my_courses': my_courses,
            'current_page': current_page,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        org_list = []
        current_page = 'myfavorg'
        fav_orgs = UserFavourite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'current_page': current_page,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        teacher_list = []
        current_page = 'myfav_teacher'
        fav_teachers = UserFavourite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            org = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(org)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'current_page': current_page,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        course_list = []
        current_page = 'myfav_course'
        fav_courses = UserFavourite.objects.filter(user=request.user, fav_type=1)
        for fav_teacher in fav_courses:
            org = Course.objects.get(id=fav_teacher.fav_id)
            course_list.append(org)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
            'current_page': current_page,
        })


class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        current_page = 'messages'
        messages = UserMessage.objects.filter(user=request.user)
        for message in messages:
            message.has_read = True
            message.save()

        # 对消息数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(messages, per_page=5, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages': messages,
            'current_page': current_page,
        })


def message_nums(request):
    '''
    定义全局变量
    :param request:
    :return:
    '''
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None