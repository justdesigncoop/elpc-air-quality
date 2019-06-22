from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^favicon\.ico$', views.FaviconView.as_view()),
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^session/(?P<pk>[0-9]+)/$', views.SessionView.as_view(), name='session'),
    #url(r'^map/$', views.MapView.as_view(), name='map'),
    url(r'^mobile_sessions/$', views.MobileSessionsView.as_view(), name='mobile_sessions'),
    url(r'^data_values/$', views.DataValuesView.as_view(), name='data_values'),
    url(r'^data_averages/$', views.DataAveragesView.as_view(), name='data_averages'),
    url(r'^coverage/$', views.CoverageView.as_view(), name='coverage'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^advocacy/$', views.AdvocacyView.as_view(), name='advocacy'),
    url(r'^results/$', views.ResultsView.as_view(), name='results'),
    url(r'^locations/$', views.LocationsView.as_view(), name='locations'),
    url(r'^partners/$', views.PartnersView.as_view(), name='partners'),
    url(r'^references/$', views.ReferencesView.as_view(), name='references'),
    url(r'^ajax/last_updated/$', views.last_updated, name='last_updated'),
    url(r'^ajax/get_users/$', views.get_users, name='get_users'),
    url(r'^ajax/get_sessions/$', views.get_sessions, name='get_sessions'),
    url(r'^ajax/get_streams/$', views.get_streams, name='get_streams'),
    url(r'^ajax/get_measurements/$', views.get_measurements, name='get_measurements'),
    url(r'^ajax/get_neighborhoods/$', views.get_neighborhoods, name='get_neighborhoods'),
    url(r'^ajax/get_tracts/$', views.get_tracts, name='get_tracts'),
    url(r'^ajax/get_wards/$', views.get_wards, name='get_wards'),
    url(r'^ajax/get_hexagons/$', views.get_hexagons, name='get_hexagons'),
    url(r'^ajax/get_zipcodes/$', views.get_zipcodes, name='get_zipcodes'),
    url(r'^ajax/get_averages/$', views.get_averages, name='get_averages'),
    url(r'^ajax/get_counts/$', views.get_counts, name='get_counts')
]
