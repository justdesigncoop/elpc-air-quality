from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /dashboard/
    url(r'^$', views.index, name='index'),
	# ex: /dashboard/5/
	url(r'^session/(?P<session_id>[0-9]+)/$', views.session, name='session'),
]
