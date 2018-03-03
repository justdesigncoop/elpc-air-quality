# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Sessions, Users

class MapForm(forms.Form):
    users = forms.MultipleChoiceField(choices=[])
    all_users = forms.BooleanField(required=False)
    keywords = forms.CharField()
    sessions = forms.MultipleChoiceField(choices=[], required=True)
    all_sessions = forms.BooleanField(required=False)
    #start_time = forms.DateTimeField(required=False)
    #end_time = forms.DateTimeField(required=False)
    
    '''
    def __init__(self, *args, **kwargs):
        super(MapForm, self).__init__(*args, **kwargs)
        
        # update fields
        self.fields['username'].choices = [(x.pk, x.username) for x in Users.objects.all()]
        self.fields['session'].choices = [(x.pk, x.title) for x in Sessions.objects.all()]
    '''
    

        
