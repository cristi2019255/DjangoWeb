
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

import mySite.mainApp.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(
            mySite.mainApp.routing.ws_urlpatterns
        ))
})