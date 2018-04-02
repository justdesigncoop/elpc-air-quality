# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core import serializers
from django.db.models import Q, Avg, Count

from .models import Users, Sessions, Streams, Measurements, Neighborhoods, Census, Wards

from .forms import MobileSessionsForm, DataValuesForm, DataAveragesForm, CoverageForm

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

class DataAveragesView(generic.FormView):
	template_name = 'dashboard/data_averages.html'
	form_class = DataAveragesForm
	success_url = '/dashboard/'

class CoverageView(generic.FormView):
	template_name = 'dashboard/coverage.html'
	form_class = CoverageForm
	success_url = '/dashboard/'

def get_users(request):
    user_ids = json.loads(request.GET.get('user_ids', '[]'))
    
    users = Users.objects.all()
    
    if user_ids:
        users = users.filter(id__in=user_ids)

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
    
    streams = Streams.objects.all()
    
    if session_ids:
        streams = streams.filter(session__in=session_ids)
    
    data = {
        'streams': serializers.serialize("json", streams)
    }
    return JsonResponse(data)

def get_measurements(request):
    stream_ids = json.loads(request.GET.get('stream_ids', '[]'))
    geo_type = json.loads(request.GET.get('geo_type', '[]'))
    geo_boundaries = json.loads(request.GET.get('geo_boundaries', '[]'))
    sample_size = json.loads(request.GET.get('sample_size', '[]'))
    min_value = json.loads(request.GET.get('min_value', '[]'))
    max_value = json.loads(request.GET.get('max_value', '[]'))
    
    if sample_size:
        measurements = Measurements.objects.raw('SELECT * FROM measurements where RAND() <= %f' % (float(sample_size)/float(Measurements.objects.count())))
    else:
        measurements = Measurements.objects.all()
    
    if stream_ids:
        measurements = measurements.filter(stream__in=stream_ids)
    
    if geo_type == 'Census':
        measurements = measurements.filter(tract__in=geo_boundaries)
    elif geo_type == 'Neighborhoods':
        measurements = measurements.filter(neighborhood__in=geo_boundaries)
    elif geo_type == 'Wards':
        measurements = measurements.filter(ward__in=geo_boundaries)
        
    if min_value:
        measurements = measurements.filter(value__gte=min_value)

    if max_value:
        measurements = measurements.filter(value__lt=max_value)
        
    data = {
        'measurements': serializers.serialize("json", measurements)
    }
    return JsonResponse(data)

def get_neighborhoods(request):
    neighborhood_ids = json.loads(request.GET.get('neighborhood_ids', '[]'))
    
    neighborhoods = Neighborhoods.objects.all()
    
    if neighborhood_ids:
        neighborhoods = neighborhoods.filter(id__in=neighborhood_ids)
    
    data = {
        'neighborhoods': serializers.serialize("json", neighborhoods)
    }
    return JsonResponse(data)

def get_census(request):
    tract_ids = json.loads(request.GET.get('tracts', '[]'))
    
    census = Census.objects.all()
    
    if tract_ids:
        census = census.filter(tract__in=tract_ids)
    
    data = {
        'census': serializers.serialize("json", census)
    }
    return JsonResponse(data)

def get_wards(request):
    ward_ids = json.loads(request.GET.get('wards', '[]'))
    
    wards = Wards.objects.all()
    
    if ward_ids:
        wards = wards.filter(ward__in=ward_ids)
    
    data = {
        'wards': serializers.serialize("json", wards)
    }
    return JsonResponse(data)

def get_averages(request):
    stream_ids = json.loads(request.GET.get('stream_ids', '[]'))
    geo_type = json.loads(request.GET.get('geo_type', '[]'))
    
    measurements = Measurements.objects.all()
    
    if stream_ids:
        measurements = measurements.filter(stream__in=stream_ids)
    
    averages = None
    
    if geo_type == 'Census':
        averages = parse_averages('tract', measurements)
    elif geo_type == 'Neighborhoods':
        averages = parse_averages('neighborhood', measurements)
    elif geo_type == 'Wards':
        averages = parse_averages('ward', measurements)
    
    data = {
        'averages': json.dumps(averages, cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)

def parse_averages(name, measurements):
    data = measurements.values(name).annotate(average=Avg('value'))
    
    averages = {}
    for d in list(data):
        n = d.pop(name)
        if n:
            averages[n] = d['average']

    return averages

def get_counts(request):
    stream_ids = json.loads(request.GET.get('stream_ids', '[]'))
    geo_type = json.loads(request.GET.get('geo_type', '[]'))
    
    measurements = Measurements.objects.all()
    
    if stream_ids:
        measurements = measurements.filter(stream__in=stream_ids)
    
    counts = None
    
    if geo_type == 'Census':
        counts = parse_counts('tract', measurements)
    elif geo_type == 'Neighborhoods':
        counts = parse_counts('neighborhood', measurements)
    elif geo_type == 'Wards':
        counts = parse_counts('ward', measurements)
    
    data = {
        'counts': json.dumps(counts, cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)

def parse_counts(name, measurements):
    data = measurements.values(name).annotate(counts=Count('value'))
    
    counts = {}
    for d in list(data):
        n = d.pop(name)
        if n:
            counts[n] = d['counts']

    return counts
