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

from .models import Users, Sessions, Streams, Measurements, Neighborhoods, Census, Wards

from .forms import MobileSessionsForm, DataValuesForm

from functools import reduce
from operator import or_

import json

class IndexView(generic.ListView):
	template_name = 'dashboard/index.html'
	context_object_name = 'latest_session_list'
	
	def get_queryset(self):
		return Sessions.objects.order_by('-updated_at')[:5]

#class SessionView(generic.DetailView):
#	template_name = 'dashboard/session.html'
#	model = Sessions

#class MapView(generic.FormView):
#	template_name = 'dashboard/map.html'
#	form_class = MapForm
#	success_url = '/dashboard/'

class MobileSessionsView(generic.FormView):
	template_name = 'dashboard/mobile_sessions.html'
	form_class = MobileSessionsForm
	success_url = '/dashboard/'
	
class DataValuesView(generic.FormView):
	template_name = 'dashboard/data_values.html'
	form_class = DataValuesForm
	success_url = '/dashboard/'

def get_users(request):
    data = {
        'users': serializers.serialize("json", Users.objects.filter())
    }
    return JsonResponse(data)

def get_sessions(request):
    user_ids = json.loads(request.GET.get('user_ids', '[]'))
    keywords = json.loads(request.GET.get('keywords', '[]'))
    
    sessions = Sessions.objects.filter()
    
    if user_ids:
        sessions = sessions.filter(user_id__in=user_ids)
    
    if keywords:
        keywords_query = [Q(title__icontains=keyword) for keyword in keywords]
        sessions = sessions.filter(reduce(or_, keywords_query))
    
    data = {
        'sessions': serializers.serialize("json", sessions)
    }
    return JsonResponse(data)

def get_streams(request):
    session_ids = json.loads(request.GET.get('session_ids', '[]'))
    data = {
        'streams': serializers.serialize("json", Streams.objects.filter(session__in=session_ids))
    }
    return JsonResponse(data)

def get_measurements(request):
    stream_ids = json.loads(request.GET.get('stream_ids', '[]'))
    neighborhood_ids = json.loads(request.GET.get('neighborhood_ids', '[]'))
    
    measurements = Measurements.objects.filter()
    
    if stream_ids:
        measurements = measurements.filter(stream__in=stream_ids)
    
    if neighborhood_ids:
        measurements = measurements.filter(neighborhood_id__in=neighborhood_ids)
    
    data = {
        'measurements': serializers.serialize("json", measurements)
    }
    return JsonResponse(data)

def get_neighborhoods(request):
    neighborhood_ids = json.loads(request.GET.get('neighborhood_ids', '[]'))
    
    neighborhoods = Neighborhoods.objects.filter()
    
    if neighborhood_ids:
        neighborhoods = neighborhoods.filter(id__in=neighborhood_ids)
    
    data = {
        'neighborhoods': serializers.serialize("json", neighborhoods)
    }
    return JsonResponse(data)
