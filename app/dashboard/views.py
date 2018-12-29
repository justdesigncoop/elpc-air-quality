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

from .models import Users, Sessions, Streams, Measurements, Neighborhoods, Tracts, Wards, Hexagons, Zipcodes

from .forms import MobileSessionsForm, DataValuesForm, DataAveragesForm, CoverageForm

from functools import reduce
from operator import or_

import json
import datetime
import random

from timeit import default_timer as timer

class FaviconView(generic.RedirectView):
    url='/static/dashboard/favicon.ico'
    permanent=True

class IndexView(generic.TemplateView):
	template_name = 'dashboard/index.html'

#class SessionView(generic.DetailView):
#	template_name = 'dashboard/session.html'
#	model = Sessions

#class MapView(generic.FormView):
#	template_name = 'dashboard/map.html'
#	form_class = MapForm
#	success_url = '/dashboard/'

class AboutView(generic.TemplateView):
	template_name = 'dashboard/about.html'

class LocationsView(generic.TemplateView):
	template_name = 'dashboard/locations.html'
	
class ResultsView(generic.TemplateView):
	template_name = 'dashboard/results.html'

class PartnersView(generic.TemplateView):
	template_name = 'dashboard/partners.html'
	
class ReferencesView(generic.TemplateView):
	template_name = 'dashboard/references.html'
	
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
    user_ids = json.loads(request.POST.get('user_ids', '[]'))
    
    users = Users.objects
    
    if user_ids:
        users = users.filter(id__in=user_ids)

    data = {
        'users': json.dumps(list(users.values('id', 'username', 'display')), cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)

def get_sessions(request):
    user_ids = json.loads(request.POST.get('user_ids', '[]'))
    keywords = json.loads(request.POST.get('keywords', '[]'))
    
    print user_ids
    print keywords
    
    sessions = Sessions.objects
    
    if user_ids:
        sessions = sessions.filter(user_id__in=user_ids)
    
    if keywords:
        keywords_query = [Q(title__icontains=keyword) for keyword in keywords]
        sessions = sessions.filter(reduce(or_, keywords_query))
    
    data = {
        'sessions': json.dumps(list(sessions.values('id', 'title')), cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)

def get_streams(request):
    session_ids = json.loads(request.POST.get('session_ids', '[]'))
    sensor_names = json.loads(request.POST.get('sensor_names', '[]'))
    sample_size = json.loads(request.POST.get('sample_size', '[]'))
    
    streams = Streams.objects
    
    if session_ids:
        streams = streams.filter(session__in=session_ids)

    if sensor_names:
        streams = streams.filter(sensor_name__in=sensor_names)   
        
    if sample_size:
        streams = streams.order_by('?')[:sample_size]
    
    print "len(streams) = " + str(len(streams))
    
    data = {
        'streams': json.dumps(list(streams.values('id')), cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)

def get_measurements(request):
    start = timer()
    stream_ids = json.loads(request.POST.get('stream_ids', '[]'))
    geo_type = json.loads(request.POST.get('geo_type', '[]'))
    geo_boundaries = json.loads(request.POST.get('geo_boundaries', '[]'))
    sample_size = json.loads(request.POST.get('sample_size', '[]'))
    min_value = json.loads(request.POST.get('min_value', '[]'))
    max_value = json.loads(request.POST.get('max_value', '[]'))
    week_day = json.loads(request.POST.get('week_day', '[]'))
    start_date = json.loads(request.POST.get('start_date', '[]'))
    end_date = json.loads(request.POST.get('end_date', '[]'))
    start_time = json.loads(request.POST.get('start_time', '[]'))
    end_time = json.loads(request.POST.get('end_time', '[]'))
    
    '''
    if sample_size:
        measurements = Measurements.objects.raw('SELECT * FROM measurements where RAND() <= %f' % (float(sample_size)/float(Measurements.objects.count())))
    else:
        measurements = Measurements.objects
    '''
    measurements = Measurements.objects
    
    if sample_size:
        measurements = measurements.order_by('?')[:sample_size]
    
    if stream_ids:
        measurements = measurements.filter(stream__in=stream_ids)
    
    if geo_type == 'tract':
        measurements = measurements.filter(tract__in=geo_boundaries)
    elif geo_type == 'neighborhood':
        measurements = measurements.filter(neighborhood__in=geo_boundaries)
    elif geo_type == 'ward':
        measurements = measurements.filter(ward__in=geo_boundaries)
        
    if min_value:
        measurements = measurements.filter(value__gte=min_value)

    if max_value:
        measurements = measurements.filter(value__lt=max_value)

    if week_day:
        measurements = measurements.filter(time__week_day__in=week_day)
    
    if start_date:
        measurements = measurements.filter(time__date__gte=datetime.datetime.strptime(start_date, "%Y-%m-%d").date())
    
    if end_date:
        measurements = measurements.filter(time__date__lte=datetime.datetime.strptime(end_date, "%Y-%m-%d").date())
    
    if start_time:
        measurements = measurements.filter(time__time__gte=datetime.datetime.strptime(start_time, "%H:%M:%S").time())
    
    if end_time:
        measurements = measurements.filter(time__time__lte=datetime.datetime.strptime(end_time, "%H:%M:%S").time())
    
    print "len(measurements) = " + str(measurements.count())
    print "filters = " + str(timer() - start)
    
    data = {
        'measurements': json.dumps(list(measurements.values('id', 'stream_id', 'value', 'latitude', 'longitude', 'time')), cls=serializers.json.DjangoJSONEncoder)
    } 
    print "json = " + str(timer() - start)
    return JsonResponse(data)

def get_neighborhoods(request):
    neighborhood_ids = json.loads(request.POST.get('neighborhood_ids', '[]'))
    
    neighborhoods = Neighborhoods.objects
    
    if neighborhood_ids:
        neighborhoods = neighborhoods.filter(id__in=neighborhood_ids)
    
    
    data = {
        'neighborhoods': json.dumps(list(neighborhoods.order_by('display').values('id', 'display', 'geo')), cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)

def get_tracts(request):
    tract_ids = json.loads(request.POST.get('tract_ids', '[]'))
    
    tracts = Tracts.objects
    
    if tract_ids:
        tracts = tracts.filter(id__in=tract_ids)
    
    data = {
        'tracts': json.dumps(list(tracts.values('id', 'display', 'geo')), cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)

def get_wards(request):
    ward_ids = json.loads(request.POST.get('ward_ids', '[]'))
    
    wards = Wards.objects
    
    if ward_ids:
        wards = wards.filter(id__in=ward_ids)
    
    data = {
        'wards': json.dumps(list(wards.values('id', 'display', 'geo')), cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)
    
def get_hexagons(request):
    hexagon_ids = json.loads(request.POST.get('hexagon_ids', '[]'))
    
    hexagons = Hexagons.objects
    
    if hexagon_ids:
        hexagons = hexagons.filter(id__in=hexagon_ids)
    
    data = {
        'hexagons': json.dumps(list(hexagons.values('id', 'display', 'geo')), cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)
    
def get_zipcodes(request):
    zipcode_ids = json.loads(request.POST.get('zipcode_ids', '[]'))
    
    zipcodes = Zipcodes.objects
    
    if zipcode_ids:
        zipcodes = zipcodes.filter(id__in=zipcode_ids)
    
    data = {
        'zipcodes': json.dumps(list(zipcodes.values('id', 'display', 'geo')), cls=serializers.json.DjangoJSONEncoder)
    }
    return JsonResponse(data)

def get_averages(request):
    start = timer()
    stream_ids = json.loads(request.POST.get('stream_ids', '[]'))
    geo_type = json.loads(request.POST.get('geo_type', '[]'))
    week_day = json.loads(request.POST.get('week_day', '[]'))
    start_date = json.loads(request.POST.get('start_date', '[]'))
    end_date = json.loads(request.POST.get('end_date', '[]'))
    start_time = json.loads(request.POST.get('start_time', '[]'))
    end_time = json.loads(request.POST.get('end_time', '[]'))
    sample_size = json.loads(request.POST.get('sample_size', '[]'))
    
    measurements = Measurements.objects
    
    if sample_size:
        pass
    #    print "sample_size = " + str(sample_size)
    #    #measurements = measurements.order_by('?')[:sample_size]
    
    if stream_ids:
        measurements = measurements.filter(stream__in=stream_ids)
        
    if week_day:
        measurements = measurements.filter(time__week_day__in=week_day)
    
    if start_date:
        measurements = measurements.filter(time__date__gte=datetime.datetime.strptime(start_date, "%Y-%m-%d").date())
    
    if end_date:
        measurements = measurements.filter(time__date__lte=datetime.datetime.strptime(end_date, "%Y-%m-%d").date())
    
    if start_time:
        measurements = measurements.filter(time__time__gte=datetime.datetime.strptime(start_time, "%H:%M:%S").time())
    
    if end_time:
        measurements = measurements.filter(time__time__lte=datetime.datetime.strptime(end_time, "%H:%M:%S").time())
    
    print "counts = " + str(measurements.count())
    print "filters = " + str(timer() - start)
    
    averages = None

    if geo_type:
        averages = parse_averages(geo_type, measurements)
        
    print "averages = " + str(timer() - start)
    
    data = {
        'averages': json.dumps(averages, cls=serializers.json.DjangoJSONEncoder)
    }
    print "json = " + str(timer() - start)
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
    start = timer()
    stream_ids = json.loads(request.POST.get('stream_ids', '[]'))
    geo_type = json.loads(request.POST.get('geo_type', '[]'))
    
    measurements = Measurements.objects
    
    if stream_ids:
        measurements = measurements.filter(stream__in=stream_ids)
    
    print "count = " + str(measurements.count())
    print "filters = " + str(timer() - start)
    
    counts = None
    
    if geo_type:
        counts = parse_counts(geo_type, measurements)
    
    print "counts = " + str(timer() - start)
    
    data = {
        'counts': json.dumps(counts, cls=serializers.json.DjangoJSONEncoder)
    }
    print "json = " + str(timer() - start)    
    return JsonResponse(data)

def parse_counts(name, measurements):
    data = measurements.values(name).annotate(counts=Count('value'))
    
    counts = {}
    for d in list(data):
        n = d.pop(name)
        if n:
            counts[n] = d['counts']

    return counts

