# -*- coding: utf-8 -*-
__author__ = 'ly'
__date__ = '2017/8/31 下午10:50'

import xadmin
from .models import Course,Lesson,Video,CourseResource

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'fav_nums', 'image', 'click_nums', 'add_time']

xadmin.site.register(Course, CourseAdmin)


class LessonAdmin(object):
    list_display = ['course','name', 'add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name', 'add_time']

xadmin.site.register(Lesson, LessonAdmin)


class VideoAdmin(object):
    list_display = ['lesson','name', 'add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson__name','name', 'add_time']

xadmin.site.register(Video, VideoAdmin)


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']

xadmin.site.register(CourseResource, CourseResourceAdmin)