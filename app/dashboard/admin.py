# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Measurements, Notes, Sessions, Streams, Users

class UserAdmin(admin.ModelAdmin):
    fields = ['id', 'username', 'display']
    list_display = ['id', 'username', 'display']

class SessionAdmin(admin.ModelAdmin):
    fields = ['id', 'user_id', 'title']
    list_display = ['id', 'user_id', 'title']

admin.site.register(Users, UserAdmin)
admin.site.register(Sessions, SessionAdmin)
