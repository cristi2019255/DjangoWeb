
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

import mainApp.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(
            mainApp.routing.ws_urlpatterns
        ))
})