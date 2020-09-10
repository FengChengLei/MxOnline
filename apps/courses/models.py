from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from apps.users.models import BaseModel
from apps.organizations.models import Teacher, CourseOrg
# Create your models here.

DEGREE_CHOICE = (
    ('cj', '初级'),
    ('zj', '中级'),
    ('gj', '高级')
)


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='讲师')
    course_org = models.ForeignKey(CourseOrg, null=True, on_delete=models.CASCADE,verbose_name='课程机构')
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    degree = models.CharField(max_length=2, choices=DEGREE_CHOICE, verbose_name='难度')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    notice = models.CharField(default='', max_length=300, verbose_name='课程公告')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', max_length=10, verbose_name='课程标签')
    youneed_now = models.CharField(default='', max_length=300, verbose_name='课程须知')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name='老师告诉你')

    detail = UEditorField(verbose_name='课程详情', width=600, height=300, imagePath='courses/ueditor/images', filePath='courses/ueditor/files', default='')
    image = models.ImageField(max_length=100, upload_to='courses/%Y/%m', verbose_name='封面图')
    is_classics = models.BooleanField(default=False, verbose_name='是否经典')
    is_banner = models.BooleanField(default=False, verbose_name='是否广告位')

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<img src="{}">'.format(self.image.url))
    # 配置xadmin中列的名称
    show_image.short_description = '图片'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="/course/{}">跳转</a>'.format(self.id))
    go_to.short_description = '跳转'



class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程') # on_delete 表示对应的外键数据被删除后，当前的数据应该如何:CASCADE或SET_NULL,null=True,blank=True
    name = models.CharField(max_length=100, verbose_name='章节名')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    tag = models.CharField(max_length=100, verbose_name='标签')

    class Meta:
        verbose_name = '课程标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True

