from django.conf.urls import url

from webApp.ws import consumers

websocket_urlpatterns = [
    url(r'^ws/poll/(?P<key>\w+)/answer/$', consumers.PollAnswerConsumer),
]
