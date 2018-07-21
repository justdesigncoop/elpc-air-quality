# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

#from .models import Sessions, Users

#dateTimeOptions = {
#    'format': 'dd/mm/yyyy HH:ii P',
#    'autoclose': True,
#    'showMeridian' : True
#}

weekDays = (
    (2, "Monday"),
    (3, "Tuesday"),
    (4, "Wednesday"),
    (5, "Thursday"),
    (6, "Friday"),
    (7, "Saturday"),
    (1, "Sunday"),
)

class MobileSessionsForm(forms.Form):
    users = forms.MultipleChoiceField(choices=[], required=True)
    all_users = forms.BooleanField(required=False)
    keywords = forms.CharField(required=False)
    sessions = forms.MultipleChoiceField(choices=[], required=True)
    #all_sessions = forms.BooleanField(required=False)
    
class DataValuesForm(forms.Form):
    users = forms.MultipleChoiceField(choices=[], required=True)
    all_users = forms.BooleanField(required=False)
    week_day = forms.MultipleChoiceField(choices=weekDays, required=False)
    start_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    end_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    start_time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
    end_time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
    pm_level = forms.ChoiceField(choices=[], required=False)
    geo_type = forms.ChoiceField(required=False)
    geo_boundaries = forms.MultipleChoiceField(choices=[], required=False)
    
class DataAveragesForm(forms.Form):
    week_day = forms.MultipleChoiceField(choices=weekDays, required=False)  
    start_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    end_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    start_time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
    end_time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
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
    

        
