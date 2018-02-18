from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^session/(?P<pk>[0-9]+)/$', views.SessionView.as_view(), name='session'),
	url(r'^map/$', views.MapView.as_view(), name='map'),
    url(r'^ajax/get_sessions/$', views.get_sessions, name='get_sessions'),
    url(r'^ajax/get_streams/$', views.get_streams, name='get_streams'),
    url(r'^ajax/get_measurements/$', views.get_measurements, name='get_measurements')
]
