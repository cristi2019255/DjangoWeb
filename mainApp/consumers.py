import base64
import json
import threading

import numpy as np
from PIL import Image
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

from .GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithm
from .PsoAlgorithm.PSO import PSO
from .convert_img_base64 import readb64, image_to_byte_array, read64_np


class GeneticImageConsumer(WebsocketConsumer):
    def __init__(self):
        self.cancel = False
        self.target_image = []
        self.shape = 'line'
        self.pop_size = 100
        self.shapes_size = 300
        self.max_iter = 1000
        self.mutation_rate = 0.3
        self.elitism_rate = 0.2
        self.resolution = 25
        self.resolver = None
        self.thread = None
        WebsocketConsumer.__init__(self)

    def connect(self):
        self.accept()

    def receive(self, text_data):
        """
        :param text_data: JSON object
        :return:
        """
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

        self.thread = threading.Thread(target=self.next)
        self.thread.start()

    def next(self):
        for _ in range(self.max_iter):
            print(iter)
            np_array_generated = self.resolver.step()
            image_generated_bytes = image_to_byte_array(Image.fromarray(np_array_generated))
            encoded_string = str(base64.b64encode(image_generated_bytes))
            self.send(json.dumps({'iteration': str(iter), 'message': encoded_string}))
            if self.cancel:
                break

    def disconnect(self, code):
        """
        When closing socket from client or something is wrong deleting thread for not running expensive operation
        on server side
        :param code:
        :return:
        """
        print('Disconnecting...')
        self.cancel = True
        del self.thread
        raise StopConsumer


class PsoImageConsumer(WebsocketConsumer):
    def __init__(self):
        self.max_iter = 150
        self.width = 128
        self.height = 128
        self.imitating_factor = 0.8
        self.cancel = False
        self.thread = None
        self.resolver = None
        self.target_image = []
        WebsocketConsumer.__init__(self)

    def connect(self):
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data_base64 = str(text_data_json['message'])
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

        self.thread = threading.Thread(target=self.next)
        self.thread.start()

    def next(self):
        for iteration in range(self.max_iter):
            print(iteration)
            np_array_generated = self.resolver.step(iteration)
            image_generated_bytes = image_to_byte_array(Image.fromarray(np_array_generated, 'HSV').convert('RGB'))
            encoded_string = str(base64.b64encode(image_generated_bytes))
            self.send(json.dumps({'iteration': str(iteration), 'message': encoded_string}))
            if self.cancel:
                break

    def disconnect(self, code):
        print('Disconnecting...')
        self.cancel = True
        del self.thread
        raise StopConsumer

class KMeansImageConsumer(WebsocketConsumer):
    def __init__(self):
        self.thread = None
        self.n_colors = 4
        self.target_image = []
        WebsocketConsumer.__init__(self)

    def connect(self):
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data_base64 = str(text_data_json['message'])
        self.n_colors = int(text_data_json['n_colors'])
        self.target_image = Image.fromarray(readb64(data_base64), 'RGB')
        self.run()

    def run(self):
        self.thread = threading.Thread(target=self.next)
        self.thread.start()

    def next(self):
        image = np.asarray(self.target_image, dtype=np.float64) / 255

        w, h, d = image.shape
        # convert to a 2d array
        image_array = np.reshape(image, (w * h, d))
        image_sample = shuffle(image_array, random_state=42)[:1000]

        # Fit kmeans
        kMeans = KMeans(n_clusters=self.n_colors, random_state=42).fit(image_sample)

        # get color indices for full image
        labels = kMeans.predict(image_array)

        segmentated_image = (255 * self.reconstruct_image(kMeans.cluster_centers_, labels, w, h)).astype(np.uint8)
        image_generated_bytes = image_to_byte_array(Image.fromarray(segmentated_image))
        encoded_string = str(base64.b64encode(image_generated_bytes))
        self.send(json.dumps({'iteration': 'KMeans image segmentation', 'message': encoded_string}))
        self.close()

    def reconstruct_image(self, cluster_centers, labels, w, h):
        d = cluster_centers.shape[1]
        image = np.zeros((w, h, d))
        label_index = 0
        for i in range(w):
            for j in range(h):
                image[i][j] = cluster_centers[labels[label_index]]
                label_index += 1
        return image

    def disconnect(self, code):
        print('Disconnecting...')
        del self.thread
        raise StopConsumer
