from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^session/(?P<pk>[0-9]+)/$', views.SessionView.as_view(), name='session'),
]
