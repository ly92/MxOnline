# -*- coding: utf-8 -*-
__author__ = 'ly'
__date__ = '2017/8/31 下午10:16'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    site_title = '顶部的名称'
    site_footer = '底部的名称'
    menu_style = 'accordion'

xadmin.site.register(views.CommAdminView, GlobalSetting)


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email','send_type', 'send_time']
    search_fields = ['code', 'email','send_type']
    list_filter = ['code', 'email','send_type', 'send_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']

xadmin.site.register(Banner, BannerAdmin)