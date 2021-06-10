from django.urls import path, re_path

from .WSConsumer import WSConsumer
from . import consumers
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter



application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(
            [
                re_path(r'ws/some_url/$', WSConsumer.as_asgi()),
                re_path(r'ws/genetic_image_consumer/$', consumers.GeneticImageConsumer.as_asgi(), name="Genetic"),
                re_path(r'ws/pso_image_consumer/$', consumers.PsoImageConsumer.as_asgi(), name="Pso"),
                #path('ws/gan_image_consumer/', GANImageConsumer.as_asgi()),
                #path('ws/can_image_consumer/', CANImageConsumer.as_asgi()),
            ]
        ))
})