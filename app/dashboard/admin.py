# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Measurements, Notes, Sessions, Streams, Users

class UserAdmin(admin.ModelAdmin):
    fields = ['id', 'username']
    list_display = ['id', 'username']

admin.site.register(Users, UserAdmin)


