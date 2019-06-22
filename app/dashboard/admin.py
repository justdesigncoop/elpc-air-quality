# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Measurements, Notes, Sessions, Streams, Users

class UserAdmin(admin.ModelAdmin):
    fields = ['id', 'username', 'display', 'private']
    list_display = ['id', 'username', 'display', 'private']

class SessionAdmin(admin.ModelAdmin):
    fields = ['id', 'title']
    list_display = ['id', 'title']

admin.site.register(Users, UserAdmin)
admin.site.register(Sessions, SessionAdmin)
