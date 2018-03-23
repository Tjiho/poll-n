from django.conf.urls import url
from webApp.views.index import index
from django.contrib.auth.views import logout



urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]


