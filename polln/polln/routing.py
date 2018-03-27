from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import webApp.routing
from channels.sessions import SessionMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': SessionMiddlewareStack(
        URLRouter(
            webApp.routing.websocket_urlpatterns
        )
    ),
})