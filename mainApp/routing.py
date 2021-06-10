from django.urls import path, re_path

from . import consumers

ws_urlpatterns = [
                re_path(r'ws/genetic_image_consumer/$', consumers.GeneticImageConsumer.as_asgi(), name="Genetic"),
                re_path(r'ws/pso_image_consumer/$', consumers.PsoImageConsumer.as_asgi(), name="Pso"),
                #path('ws/gan_image_consumer/', GANImageConsumer.as_asgi()),
                #path('ws/can_image_consumer/', CANImageConsumer.as_asgi()),
                ]