import os
import django
from channels.routing import get_default_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

import mainApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySite.settings')
django.setup()

application = ProtocolTypeRouter({
    'http': get_default_application(),
    'websocket': AuthMiddlewareStack(URLRouter(
            mainApp.routing.ws_urlpatterns
        ))
})