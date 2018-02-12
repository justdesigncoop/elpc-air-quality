# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Sessions


class IndexView(generic.ListView):
	template_name = 'dashboard/index.html'
	context_object_name = 'latest_session_list'
	
	def get_queryset(self):
		return Sessions.objects.order_by('-updated_at')[:5]

class SessionView(generic.DetailView):
	template_name = 'dashboard/session.html'
	model = Sessions
