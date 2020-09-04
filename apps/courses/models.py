from datetime import datetime

from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
# Create your models here.

DEGREE_CHOICE = (
    ('cj', '初级'),
    ('zj', '中级'),
    ('gj', '高级')
)


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='讲师')
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    degree = models.CharField(max_length=2, choices=DEGREE_CHOICE, verbose_name='难度')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', max_length=10, verbose_name='课程标签')
    youneed_now = models.CharField(default='', max_length=300, verbose_name='课程须知')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name='老师告诉你')

    detail = models.TextField(verbose_name='课程详情')
    image = models.ImageField(max_length=100, upload_to='courses/%Y/%m',verbose_name='封面图')

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    # def __str__(self):


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # on_delete 表示对应的外键数据被删除后，当前的数据应该如何:CASCADE或SET_NULL,null=True,blank=True
    name = models.CharField(max_length=100, verbose_name='章节名')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='视频名')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    url = models.CharField(max_length=200, verbose_name='访问地址')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    file = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='下载地址', max_length=200)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
