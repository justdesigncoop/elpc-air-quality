# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Measurements, Notes, Sessions, Streams, Users

admin.site.register(Measurements)
admin.site.register(Notes)
admin.site.register(Sessions)
admin.site.register(Streams)
admin.site.register(Users)

