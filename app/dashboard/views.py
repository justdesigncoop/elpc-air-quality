# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core import serializers

from .models import Sessions
from .forms import MapForm

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

def get_session(request):
    session_id = request.GET.get('session_id', None)
    data = {
        'session': serializers.serialize("json", Sessions.objects.filter(id=session_id))
    }
    return JsonResponse(data)
