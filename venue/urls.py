from django.conf.urls import patterns, url

from venue import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^newcompany', views.newcompany, name='newcompany'),
    url(r'^newvenue', views.newvenue, name='newvenue'),
    url(r'^newevent', views.newevent, name='newevent'),
    url(r'^newguestlist/(?P<event>\w+)$', views.newguestlist, name='newguestlist'),
    url(r'^joinguestlist/(?P<guestlist>\w+)$', views.joinguestlist, name='joinguestlist'),
    url(r'^testpage', views.testpage, name='testpage'),
    url(r'^exportcsv/(?P<guestlist>\w+)$', views.exportcsv, name='exportcsv'),
    url(r'^event/(?P<event>\w+)$', views.viewevent, name='viewevent'),
    url(r'^viewguestlist/(?P<guestlist>\w+)$', views.viewguestlist, name='viewguestlist'),
    url(r'^(?P<company>\w+)$', views.company, name='company'),
    url(r'^(?P<company>\w+)/(?P<venue>\w+)$', views.venue, name='venue'),

)

# url(r'^userdb/(?P<username>\w+)$', views.userdb, name='userdb'),
# url(r'^userdb/(?P<username>\w+)/(?P<tag>\w+)$', views.userdb, name='usertag'),
# url(r'^user/(?P<username>\w+)/account$', views.useraccount, name='useraccount'),
