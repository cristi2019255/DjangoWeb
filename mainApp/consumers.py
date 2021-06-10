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
        self.target_image = readb64(data_base64)
        self.shape = str(text_data_json['shape'])
        self.pop_size = int(text_data_json['pop_size'])
        self.shapes_size = int(text_data_json['shapes_size'])
        self.resolution = int(text_data_json['resolution'])
        self.max_iter = int(text_data_json['max_iter'])
        self.elitism_rate = float(text_data_json['elitism_rate'])
        self.mutation_rate = float(text_data_json['mutation_rate'])
        self.run()

    def run(self):
        self.resolver = GeneticAlgorithm(self.pop_size,
                                         self.target_image,
                                         shape=self.shape,
                                         shapes_size=self.shapes_size,
                                         resolution=self.resolution,
                                         max_iter=self.max_iter,
                                         elitism_rate=self.elitism_rate,
                                         mutation_rate=self.mutation_rate)

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
        self.max_iter = int(text_data_json['max_iter'])
        self.width = int(text_data_json['width'])
        self.height = int(text_data_json['height'])
        self.imitating_factor = float(text_data_json['imitating_factor'])

        if data_base64 != "cancel":
            self.target_image = Image.fromarray(read64_np(data_base64,self.width,self.height), 'RGB')
            self.run()

    def run(self):
        self.resolver = PSO(width=self.width, height=self.height,
                            max_iter=self.max_iter,
                            target_image=self.target_image,
                            imitating_factor=self.imitating_factor, imitating=True)

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
