import xadmin

from django.contrib import admin

from apps.organizations.models import Teacher, CourseOrg,City
# Register your models here.


class TeacherAdmin():
    # 配置显示列
    list_display = ['org', 'name', 'work_years', 'work_company']
    # 可用于搜索的字段
    search_fields = ['org', 'name', 'work_years', 'work_company']
    # 过滤器设置
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CourseOrgAdmin():
    # 配置显示列
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    # 可用于搜索的字段
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    # 过滤器设置
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']


class CityAdmin():
    # 配置显示列
    list_display = ['id', 'name', 'desc']
    # 可用于搜索的字段
    search_fields = ['name', 'desc']
    # 过滤器设置
    list_filter = ['name', 'desc', 'add_time']
    # 可编辑按钮
    list_editable = ['name', 'desc']


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)