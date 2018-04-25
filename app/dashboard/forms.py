# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

#from .models import Sessions, Users

class MobileSessionsForm(forms.Form):
    users = forms.MultipleChoiceField(choices=[], required=True)
    all_users = forms.BooleanField(required=False)
    keywords = forms.CharField(required=False)
    sessions = forms.MultipleChoiceField(choices=[], required=True)
    #all_sessions = forms.BooleanField(required=False)
    #start_time = forms.DateTimeField(required=False)
    #end_time = forms.DateTimeField(required=False)
    
class DataValuesForm(forms.Form):
    users = forms.MultipleChoiceField(choices=[], required=True)
    all_users = forms.BooleanField(required=False)
    #start_time = forms.DateTimeField(required=False)
    #end_time = forms.DateTimeField(required=False)
    pm_level = forms.ChoiceField(choices=[], required=False)
    geo_type = forms.ChoiceField(required=False)
    geo_boundaries = forms.MultipleChoiceField(choices=[], required=False)
    
class DataAveragesForm(forms.Form):
    #start_time = forms.DateTimeField(required=False)
    #end_time = forms.DateTimeField(required=False)
    geo_type = forms.ChoiceField(required=True)

class CoverageForm(forms.Form):
    users = forms.MultipleChoiceField(choices=[], required=True)
    all_users = forms.BooleanField(required=False)
    geo_type = forms.ChoiceField(required=True)
    
'''
class MapForm(forms.Form):
    users = forms.MultipleChoiceField(choices=[], required=True)
    all_users = forms.BooleanField(required=False)
    keywords = forms.CharField(required=False)
    sessions = forms.MultipleChoiceField(choices=[], required=True)
    all_sessions = forms.BooleanField(required=False)
    #start_time = forms.DateTimeField(required=False)
    #end_time = forms.DateTimeField(required=False)
    
    
    def __init__(self, *args, **kwargs):
        super(MapForm, self).__init__(*args, **kwargs)
        
        # update fields
        self.fields['username'].choices = [(x.pk, x.username) for x in Users.objects.all()]
        self.fields['session'].choices = [(x.pk, x.title) for x in Sessions.objects.all()]
'''
    

        
