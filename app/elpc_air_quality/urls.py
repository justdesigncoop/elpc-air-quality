"""elpc_air_quality URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import login, logout

from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'', include('dashboard.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login, {'template_name': 'dashboard/login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/')),
    url(r'^accounts/$', RedirectView.as_view(url='/')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



