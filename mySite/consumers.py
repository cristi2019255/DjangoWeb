import base64
import json
import threading

from PIL import Image
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

from .GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithm
from .PsoAlgorithm.PSO import PSO
from .convert_img_base64 import readb64, image_to_byte_array, read64_np


class GeneticImageConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.cancel = False

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data_base64 = str(text_data_json['message'])

        if data_base64 == "cancel":
            print(data_base64)
        else:
            self.target_image = readb64(data_base64)
            self.run()

    def run(self):

        shape = "line"
        pop_size = 100
        shapes_size = 300
        resolution = 25
        max_iter = 1000
        elitism_rate = 0.2
        mutation_rate = 0.3

        image = self.target_image

        self.resolver = GeneticAlgorithm(pop_size, image, shape=shape, shapes_size=shapes_size, resolution=resolution,
                                    max_iter=max_iter, elitism_rate=elitism_rate, mutation_rate=mutation_rate)

        self.thread = threading.Thread(target=self.next)  # This thread will work same but
        self.thread.start()  # also allows to call disconnect()

    def next(self):
        for iter in range(10000):
            print(iter)
            np_array_generated = self.resolver.step()
            image_generated_bytes = image_to_byte_array(Image.fromarray(np_array_generated))
            encoded_string = str(base64.b64encode(image_generated_bytes))
            self.send(json.dumps({'iteration': str(iter), 'message': encoded_string}))
            if self.cancel:
                break

    def disconnect(self, code):
        print('Disconecting...')
        self.cancel = True
        del self.thread
        raise StopConsumer

class PsoImageConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.cancel = False

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data_base64 = str(text_data_json['message'])

        if data_base64 != "cancel":
            self.target_image = Image.fromarray(read64_np(data_base64), 'RGB')
            self.target_image.resize((128, 128))
            self.run()

    def run(self):
        imitation_factor = 0.8

        target_image = self.target_image

        self.resolver = PSO(width=128, height=128,
                            target_image=target_image, imitating_factor=imitation_factor, imitating=True)

        self.thread = threading.Thread(target=self.next)  # This thread will work same but
        self.thread.start()  # also allows to call disconnect()

    def next(self):
        for iter in range(150):
            print(iter)
            np_array_generated = self.resolver.step(iter)
            image_generated_bytes = image_to_byte_array(Image.fromarray(np_array_generated, 'HSV').convert('RGB'))
            encoded_string = str(base64.b64encode(image_generated_bytes))
            self.send(json.dumps({'iteration': str(iter), 'message': encoded_string}))
            if self.cancel:
                break

    def disconnect(self, code):
        print('Disconecting...')
        self.cancel = True
        del self.thread
        raise StopConsumer
