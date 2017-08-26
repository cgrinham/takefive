from django.conf.urls import patterns, url

from home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)

# url(r'^userdb/(?P<username>\w+)$', views.userdb, name='userdb'),
# url(r'^userdb/(?P<username>\w+)/(?P<tag>\w+)$', views.userdb, name='usertag'),
# url(r'^user/(?P<username>\w+)/account$', views.useraccount, name='useraccount'),
