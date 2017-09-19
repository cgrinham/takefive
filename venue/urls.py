from django.conf.urls import patterns, url, include
from django.contrib import auth


from venue import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^door/(?P<event>\w+)/$', views.door, name='door'),
    url(r'^newcompany/', views.newcompany, name='newcompany'),
    url(r'^join/', views.newmember, name='newmember'),
    url(r'^newguestlist/(?P<event>\w+)/$', views.newguestlist, name='newguestlist'),
    url(r'^joinguestlist/(?P<guestlist>\w+)/$', views.joinguestlist, name='joinguestlist'),
    url(r'^testpage', views.testpage, name='testpage'),
    url(r'^exportcsv/(?P<guestlist>\w+)/$', views.exportcsv, name='exportcsv'),
    url(r'^(?P<company>\w+)/$', views.company, name='company'),
    url(r'^(?P<company>\w+)/newvenue/$', views.newvenue, name='newvenue'),
    url(r'^(?P<company>\w+)/(?P<venue>\w+)/$', views.venue, name='venue'),
    url(r'^(?P<company>\w+)/(?P<venue>\w+)/event/(?P<event>\w+)/$', views.viewevent, name='viewevent'),
    url(r'^(?P<company>\w+)/(?P<venue>\w+)/guestlist/(?P<guestlist>\w+)/$', views.viewguestlist, name='viewguestlist'),
    url(r'^(?P<company>\w+)/(?P<venue>\w+)/newevent/$', views.newevent, name='newevent'),
    url(r'^(?P<company>\w+)/(?P<venue>\w+)/members/$', views.members, name='members'),
    url(r'^(?P<company>\w+)/(?P<venue>\w+)/layout/$', views.venuelayout, name='venuelayout'),
    url(r'^(?P<company>\w+)/(?P<venue>\w+)/layout/create/$', views.newvenuelayout, name='newvenuelayout'),
)
