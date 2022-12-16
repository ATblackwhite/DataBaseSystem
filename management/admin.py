from django.contrib import admin

from .models import *

admin.site.site_header = '管理系统后台'
admin.site.site_title = '管理系统'
admin.site.register([Member, Club, Join, Activity, Attend])
# Register your models here.
