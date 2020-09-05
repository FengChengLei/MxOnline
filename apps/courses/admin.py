import xadmin

from django.contrib import admin

from apps.courses.models import Course, Lesson, Video, CourseResource
# Register your models here.


class GlabalSettings():
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    # 折叠左侧栏
    menu_style = 'accordion'


class BaseSettings():
    enable_themes = True
    use_bootswatch = True


class CourseAdmin():
    # 配置显示列
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 可用于搜索的字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    # 过滤器设置
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 可编辑按钮
    list_editable = ['degree', 'desc']


class LessonAdmin():
    # 配置显示列
    list_display = ['course', 'name', 'add_time']
    # 可用于搜索的字段
    search_fields = ['course', 'name']
    # 过滤器设置,course__name:对于外键course，如果相对于course的name进行过滤，可以通过__来指定
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin():
    # 配置显示列
    list_display = ['lesson', 'name', 'add_time']
    # 可用于搜索的字段
    search_fields = ['lesson', 'name']
    # 过滤器设置
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin():
    # 配置显示列
    list_display = ['course', 'name', 'download', 'add_time']
    # 可用于搜索的字段
    search_fields = ['course', 'name', 'download']
    # 过滤器设置
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlabalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)