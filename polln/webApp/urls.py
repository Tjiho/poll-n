from django.conf.urls import url
from webApp.views.index import Index
from webApp.views.home import Home
from django.contrib.auth.views import logout



urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]


