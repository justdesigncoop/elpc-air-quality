# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core import serializers
from django.db.models import Q

from .models import Users, Sessions, Streams, Measurements

from .forms import MapForm

import json

class IndexView(generic.ListView):
	template_name = 'dashboard/index.html'
	context_object_name = 'latest_session_list'
	
	def get_queryset(self):
		return Sessions.objects.order_by('-updated_at')[:5]

class SessionView(generic.DetailView):
	template_name = 'dashboard/session.html'
	model = Sessions

class MapView(generic.FormView):
	template_name = 'dashboard/map.html'
	form_class = MapForm
	success_url = '/dashboard/'

def get_users(request):
    data = {
        'users': serializers.serialize("json", Users.objects.filter())
    }
    return JsonResponse(data)

def get_sessions(request):
    user_ids = json.loads(request.GET.get('user_ids', None))
    data = {
        'sessions': serializers.serialize("json", Sessions.objects.filter(user_id__in=user_ids))
    }
    return JsonResponse(data)

def get_streams(request):
    sessions_ids = json.loads(request.GET.get('sessions_ids', None))
    data = {
        'streams': serializers.serialize("json", Streams.objects.filter(session__in=sessions_ids))
    }
    return JsonResponse(data)

def get_measurements(request):
    stream_ids = json.loads(request.GET.get('stream_ids', None))
    data = {
        'measurements': serializers.serialize("json", Measurements.objects.filter(stream__in=stream_ids))
    }
    return JsonResponse(data)


