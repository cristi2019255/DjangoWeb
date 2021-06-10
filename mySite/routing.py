from django.urls import path

from .CANConsumer import CANImageConsumer
from .GANConsumer import GANImageConsumer
from .PsoImageConsumer import PsoImageConsumer
from .WSConsumer import WSConsumer
from .GeneticImageConsumer import GeneticImageConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

ws_urlpatterns = [
    path('ws/some_url/', WSConsumer.as_asgi()),
    path('ws/genetic_image_consumer/', GeneticImageConsumer.as_asgi()),
    path('ws/pso_image_consumer/', PsoImageConsumer.as_asgi()),
    path('ws/gan_image_consumer/', GANImageConsumer.as_asgi()),
    path('ws/can_image_consumer/', CANImageConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})