from django.urls import path


from .WSConsumer import WSConsumer
from . import consumers
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter



application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(
            [
                path('ws/some_url/', WSConsumer.as_asgi()),
                path('ws/genetic_image_consumer/', consumers.GeneticImageConsumer, name="Genetic"),
                path('ws/pso_image_consumer/', consumers.PsoImageConsumer, name="Pso"),
                #path('ws/gan_image_consumer/', GANImageConsumer.as_asgi()),
                #path('ws/can_image_consumer/', CANImageConsumer.as_asgi()),
            ]
        ))
})