import xadmin

from django.contrib import admin
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper
from import_export import resources

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, BannerCourse
# Register your models here.


class LessonInline():
    model = Lesson
    extra = 0
    # 显示样式
    style = 'tab'

class CourseResourceInline():
    model = CourseResource
    extra = 1
    style = 'tab'
    # 不显示字段
    exclude = ['add_time']

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


class MyResource(resources.ModelResource):
    class Meta:
        model = Course


class NewCourseAdmin():
    import_export_args = {'import_resource_class': MyResource,'export_resource_class': MyResource}
    # 配置显示列
    list_display = ['name', 'desc', 'show_image', 'detail', 'degree', 'learn_times', 'students', 'go_to']
    # 可用于搜索的字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    # 过滤器设置
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 可编辑按钮
    list_editable = ['degree', 'desc']
    # 只读：无法修改的数据
    readonly_fields = ['click_nums', 'fav_nums', 'students']
    # 页面不显示数据
    exclude = ['add_time']
    # 列表排序
    ordering = ['click_nums']
    # 设置图标
    model_icon = 'fa fa-address-book'
    # 在课程页面编辑课程资源
    inlines = [LessonInline, CourseResourceInline]
    # xadmin中使用ueditor
    style_fields = {
        'detail': 'ueditor'
    }

    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset('讲师信息',
                         'teacher', 'course_org',
                         css_class='unsort no_title'),
                Fieldset('基本信息',
                         'name', 'desc',
                         Row('learn_times', 'degree'),
                         Row('category', 'tag'),
                         'youneed_now', 'teacher_tell', 'detail',
                         css_class='unsort no_title')
            ),
            Side(
                Fieldset(
                    '访问信息',
                    'fav_nums', 'click_nums', 'students'
                )
            ),
            Side(
                Fieldset(
                    '选择信息',
                    'is_banner', 'is_classics'
                )
            )
        )
        return super(NewCourseAdmin, self).get_form_layout()


class BannerCourseAdmin():
    # 配置显示列
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 可用于搜索的字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    # 过滤器设置
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    # 可编辑按钮
    list_editable = ['degree', 'desc']

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


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
    list_display = ['course', 'name', 'file', 'add_time']
    # 可用于搜索的字段
    search_fields = ['course', 'name', 'file']
    # 过滤器设置
    list_filter = ['course', 'name', 'file', 'add_time']


class CourseTagAdmin():
    # 配置显示列
    list_display = ['course', 'tag', 'add_time']
    # 可用于搜索的字段
    search_fields = ['course', 'tag']
    # 过滤器设置
    list_filter = ['course', 'tag', 'add_time']




# xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Course, NewCourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlabalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)