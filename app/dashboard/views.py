# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render

from .models import Sessions


def index(request):
    latest_session_list = Sessions.objects.order_by('-updated_at')[:5]
    template = loader.get_template('dashboard/index.html')
    context = {
        'latest_session_list': latest_session_list,
    }
    return render(request, 'dashboard/index.html', context)

def session(request, session_id):
    session = get_object_or_404(Sessions, pk=session_id)
    return render(request, 'dashboard/session.html', {'session': session})
