
import base64
import json
import os

import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from channels.generic.websocket import WebsocketConsumer
from .convert_img_base64 import readb64, image_to_byte_array
import torch.nn as nn


def denomralization(img_tensors):
    return img_tensors * 0.5 + 0.5


def to_device(data, device):
    """Move tensors to chosen device"""
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)


def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    return torch.device('cpu')


def build_generator_for_GAN_model(latent_size):
    model = nn.Sequential(

        # input: latent_size x 1 x 1
        nn.ConvTranspose2d(latent_size, 512, kernel_size=4, stride=1, padding=0, bias=False),
        nn.BatchNorm2d(512),
        nn.ReLU(),
        # output: 512 x 4 x 4

        nn.ConvTranspose2d(512, 256, kernel_size=4, stride=2, padding=1, bias=False),
        nn.BatchNorm2d(256),
        nn.ReLU(),
        # output: 256 x 8 x 8

        nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1, bias=False),
        nn.BatchNorm2d(128),
        nn.ReLU(),
        # output: 128 x 16 x 16

        nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1, bias=False),
        nn.BatchNorm2d(64),
        nn.ReLU(),
        # output: 64 x 32 x 32

        nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2, padding=1, bias=False),
        nn.BatchNorm2d(32),
        nn.ReLU(True),
        # output: 32 x 64 x 64

        nn.ConvTranspose2d(32, 3, kernel_size=4, stride=2, padding=1, bias=False),
        nn.Tanh()
        # out: 3 x 128 x 128
    )
    return model


class GANImageConsumer(WebsocketConsumer):
    def __init__(self):
        self.cancel = False
        WebsocketConsumer.__init__(self)

    def connect(self):
        self.accept()
        generator = build_generator_for_GAN_model(200)

        generator.load_state_dict(
            torch.load( "C:\\Users\\Asus\\PycharmProjects\\mySite\\mySite\\mySite\\G_gan.ckpt",
                       map_location='cpu'))
        latent_tensor = torch.randn(1, 200, 1, 1)
        fake_image = generator(latent_tensor)
        fake_image = denomralization(fake_image).detach()[0]
        fake_image = fake_image.permute(1, 2, 0).numpy()
        np_arr = (np.asarray(fake_image) * 255).astype(np.uint8)

        image_generated_bytes = image_to_byte_array(Image.fromarray(np_arr))
        encoded_string = str(base64.b64encode(image_generated_bytes))
        self.send(json.dumps({'iteration': 'Model is pretrained', 'message': encoded_string}))
