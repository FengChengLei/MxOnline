import xadmin

from django.contrib import admin

from apps.operations.models import UserAsk, CourseComments, UserCourse, UserFavourite, UserMessage, Banner


# Register your models here.


class UserAskAdmin():
    # 配置显示列
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    # 可用于搜索的字段
    search_fields = ['name', 'mobile', 'course_name']
    # 过滤器设置
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class UserCourseAdmin():
    # 配置显示列
    list_display = ['user', 'course', 'add_time']
    # 可用于搜索的字段
    search_fields = ['user', 'course']
    # 过滤器设置
    list_filter = ['user', 'course', 'add_time']

    def save_models(self):
        obj = self.new_obj
        if not obj.id:
            # 判断是否为新增数据
            obj.save()
            course = obj.course
            course.students += 1
            # 可以增加其他逻辑，例如用户消息：欢迎进入此课程
            course.save()


class UserMessageAdmin():
    # 配置显示列
    list_display = ['user', 'message', 'has_read', 'add_time']
    # 可用于搜索的字段
    search_fields = ['user', 'message', 'has_read']
    # 过滤器设置
    list_filter = ['user', 'message', 'has_read', 'add_time']


class CourseCommentsAdmin():
    # 配置显示列
    list_display = ['user', 'course', 'comments', 'add_time']
    # 可用于搜索的字段
    search_fields = ['user', 'course', 'comments']
    # 过滤器设置
    list_filter = ['user', 'course', 'comments', 'add_time']


class UserFavouriteAdmin():
    # 配置显示列
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    # 可用于搜索的字段
    search_fields = ['user', 'fav_id', 'fav_type']
    # 过滤器设置
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']

class BannerAdmin():
    # 配置显示列
    list_display = ['title', 'image', 'url', 'index']
    # 可用于搜索的字段
    search_fields = ['title', 'image', 'url', 'index']
    # 过滤器设置
    list_filter = ['title', 'image', 'url', 'index']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavourite, UserFavouriteAdmin)
xadmin.site.register(Banner, BannerAdmin)
