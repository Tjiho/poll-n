from django.conf.urls import url
from webApp.views.index import Index
from webApp.views.home import Home
from webApp.views.poll import Poll
from django.contrib.auth.views import logout



urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^poll/(?P<key>\w+)/$', Poll.as_view(), name='poll'),
    url(r'^poll/$', Poll.as_view(), name='poll'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]


