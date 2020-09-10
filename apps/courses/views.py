from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from apps.courses.models import Course, CourseTag, CourseResource,Video
from apps.operations.models import UserFavourite, UserCourse, CourseComments
# Create your views here.


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        '''获取课程列表信息'''
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")[:3]
        # 搜索关键词
        s_type = 'course'
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=5, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
            'keywords': keywords,
            's_type': s_type,
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        '''
        获取课程详情
        '''
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavourite.objects.filter(user=request.user, fav_id=course.course_org_id, fav_type=2):
                has_fav_org = True

        # 通过课程tag做课程的推荐

        # 使用内置字段标签
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     #查询相关课程并排除当前课程
        #     related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course.id])[:3]

        # 使用外键标签
        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]
        # tag_list = []
        # for tag in tags:
        #     tag_list.append(tag.tag)

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        return render(request, 'course-detail.html', {
            'course': course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'related_courses': related_courses,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        '''
        获取课程章节信息
        '''
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()
        course_resource = CourseResource.objects.filter(course=course)

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        return render(request, 'course-video.html', {
            'course': course,
            'course_resource': course_resource,
            'related_courses': related_courses
        })


class CourseCommentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        '''
        获取课程章节信息
        '''
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()
        course_resource = CourseResource.objects.filter(course=course)

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resource': course_resource,
            'related_courses': related_courses,
            'comments': comments,
        })


class VideoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, video_id, *args, **kwargs):
        '''
        获取课程章节信息
        '''
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()
        course_resource = CourseResource.objects.filter(course=course)

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('-course__click_nums')
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        return render(request, 'course-play.html', {
            'course': course,
            'course_resource': course_resource,
            'related_courses': related_courses,
            'video': video
        })