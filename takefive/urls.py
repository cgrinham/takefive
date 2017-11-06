"""takefive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
import venue
from venue.views import EventViewSet, GuestViewSet, GuestListViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'guests', GuestViewSet)
router.register(r'guestlists', GuestListViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('home.urls', namespace='home')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^venues/', include('venue.urls', namespace='venue')),
    url(r'^gl/(?P<guestlist>\w+)/$', venue.views.join_guestlist, name='join_guestlist'),
    url(r'^glr/(?P<event>\w+)/$', venue.views.join_recurring_guestlist, name='join_recurring_guestlist'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^signup/$', venue.views.signup, name='signup'),
]
