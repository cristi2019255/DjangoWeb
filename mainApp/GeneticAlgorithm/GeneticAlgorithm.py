import copy
from random import shuffle
import cv2
import numpy as np


class GeneticAlgorithm:
    def __init__(self, pop_size, image, shape, shapes_size, resolution,
                 mutation_rate=0.3, max_iter=10000, elitism_rate=0.2):
        """
        :param pop_size: population size
        :param image: target image
        :param shape: shape added at each mutation
        :param shapes_size: how many shapes are on a image of a genome
        :param resolution: different meaning for different shapes, see Genome class
        :param mutation_rate: mutation rate
        :param max_iter: maximum number of iterations
        :param elitism_rate: elitism rate
        """
        self.probability_wheel = []
        self.pop_size = pop_size
        self.image = image
        self.population = []
        self.mutation_rate = mutation_rate
        self.shape = shape
        self.shapes_size = shapes_size
        self.resolution = resolution
        self.max_iter = max_iter
        self.elitism_rate = elitism_rate
        self.create_population()

    def create_population(self):
        """
        initializing genetic algorithm population
        each individual is initialized with a random image
        :return:
        """
        for _ in range(self.pop_size):
            genome = Genome(self.image.shape[:-1],
                            shape=self.shape,
                            shapes_size=self.shapes_size,
                            resolution=self.resolution)
            genome.create_random_image()
            self.population.append(genome)

    def step(self):
        self.evaluate_fitnesses()
        self.evaluate_probability_wheel()

        self.population.sort(key=lambda x: x.fitness, reverse=True)
        self.best_genome = self.population[0]
        new_population = copy.deepcopy(self.population[:int(self.elitism_rate * self.pop_size)])
        shuffle(self.population)

        for i in range(int((1 - self.elitism_rate) * self.pop_size)):
            parent1 = self.selection()
            parent2 = self.selection()
            child = self.reproduce(parent1, parent2)

            if (np.random.random() < self.mutation_rate):
                self.mutate(child)
            new_population.append(child)

        self.population = []
        self.population = new_population
        # cv2.imwrite('../../media/' + "/Step_" + str(np.random.randint(1, 100)) + ".jpg", self.best_genome.image)
        return self.best_genome.image

    def resolve(self):
        for iter in range(self.max_iter):
            self.step()
            if (iter + 1) % 500 == 0:
                cv2.imwrite('../../media/' + "/Step_" + str(iter + 1) + ".jpg", self.best_genome.image)
            return self.best_genome.fitness

    def reproduce(self, parent1, parent2):
        """
        Produces a child genome from 2 parents
        :param parent1:
        :param parent2:
        :return: child
        """
        child = Genome(self.image.shape[:-1], shape=self.shape,
                       shapes_size=self.shapes_size,
                       resolution=self.resolution)

        weight = np.random.random()
        new_image = np.zeros(self.image.shape, dtype=np.uint8)

        # convex interpolation of parents images
        cv2.addWeighted(parent1.image, weight, parent2.image, 1 - weight, 0, new_image)
        child.image = new_image
        return child

    def mutate(self, genome):
        """
        apply mutations on image of the genome random number of times
        :param genome:
        :return:
        """
        for _ in range(np.random.randint(1, 3)):
            genome.shape_functions_dict[self.shape]()

    def evaluate_fitnesses(self):
        """
        calculating fitness of individuals with get_distance function
        we maximize fitness function
        :return:
        """
        for index, genome in enumerate(self.population):
            genome.fitness = (1. / self.get_distance(index))

    def get_distance(self, index):
        """
        calculating the distance of a genome from population to the target image
        by getting the matrix difference in Frobenius norm divided by height*width of target image
        :param index: the index of the genome we calculate distance in population
        :return: distance value
        """
        return (np.linalg.norm(self.image.astype('float') - self.population[index].image.astype('float'))) / (
                self.image.shape[0] * self.image.shape[1])

    def selection(self):
        """

        :return:
        """
        if len(self.probability_wheel) == 0:
            return self.population[np.random.randint(0, self.pop_size - 1)]
        return self.probability_wheel[np.random.randint(0, len(self.probability_wheel) - 1)]

    def evaluate_probability_wheel(self):
        """
        generating probability wheel for "roulette selection"
        :return:
        """
        total_fitness = sum(genome.fitness for genome in self.population)

        for genome in self.population:
            if genome.fitness != 0 and total_fitness != 0:
                genome.percent = int(1 + (genome.fitness / total_fitness) * 100)
            else:
                genome.percent = 1

        self.probability_wheel = []
        for genome in self.population:
            for _ in range(genome.percent):
                self.probability_wheel.append(genome)
        shuffle(self.probability_wheel)


class Genome:
        def __init__(self, image_size, shapes_size, shape='circle', resolution=10):
            """

            :param image_size: [height,width] of image of genome
            :param shapes_size: how many shapes an image have
            :param shape: what type of shapes
            :param resolution: different meaning for different shapes see associated
                                functions like add_line, add_circle,add_rectangle,...
            """
            self.shapes_size = shapes_size
            self.shape = shape

            self.height = image_size[0]
            self.width = image_size[1]

            self.shape_functions_list = ['line', 'circle', 'rectangular']
            self.shape_functions_dict = {'line': self.add_line, 'circle': self.add_circle,
                                         'rectangular': self.add_rectangle}

            self.image = []
            self.fitness = 0
            self.percent = 0

            self.shape_list = []
            self.resolution = resolution

        def create_random_image(self):
            """
            creating a black image and adding shapes on it
            :return: black image with shapes
            """
            self.image = np.zeros((self.height, self.width, 3), np.uint8)

            for _ in range(self.shapes_size):
                self.shape_functions_dict[self.shape]()

        def add_line(self):
            """
            mutation with adding a line segment
            :return:
            """

            min_x = np.random.randint(0, self.width)
            min_y = np.random.randint(0, self.height)

            max_x = min_x + np.random.randint(-1, 2) * np.random.randint(5, int(self.width / 5.))
            max_y = min_y + np.random.randint(-1, 2) * np.random.randint(5, int(self.height / 5.))

            opacity = np.random.rand(1)[0]
            thickness = np.random.randint(1, 5)

            overlay = self.image.copy()
            cv2.line(overlay, (min_x, min_y), (max_x, max_y), self.get_color(), thickness)
            cv2.addWeighted(overlay, opacity, self.image, 1 - opacity, 0, self.image)

        def add_circle(self):
            """
            mutation with adding a circle
            :return:
            """

            center_x = np.random.randint(0, self.width)
            center_y = np.random.randint(0, self.height)
            radius = np.random.randint(0, int(self.height / (1.1 * self.resolution)))
            opacity = np.random.rand(1)[0]

            overlay = self.image.copy()
            cv2.circle(overlay, (center_x, center_y), radius, self.get_color(), -1)
            cv2.addWeighted(overlay, opacity, self.image, 1 - opacity, 0, self.image)

        def add_rectangle(self):
            """
            mutation with adding a rectangle of genome image
            :return:
            """
            min_x = np.random.randint(0, self.width)
            max_x = min_x + np.random.randint(5, int(self.width / self.resolution))
            min_y = np.random.randint(0, self.height)
            max_y = min_y + np.random.randint(5, int(self.height / self.resolution))
            opacity = np.random.rand(1)[0]

            overlay = self.image.copy()
            cv2.rectangle(overlay, (min_x, min_y), (max_x, max_y), self.get_color(), -1)
            cv2.addWeighted(overlay, opacity, self.image, 1 - opacity, 0, self.image)

        @staticmethod
        def get_color():
            """
            :return: a random rgb color
            """
            return np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)


def resolve(image_path):
    shape = "line"
    pop_size = 100
    shapes_size = 300
    resolution = 50
    max_iter = 1000
    elitism_rate = 0.05
    mutation_rate = 0.3

    image = cv2.imread(image_path)
    image = cv2.resize(image, (64, 64))

    resolver = GeneticAlgorithm(pop_size, image, shape=shape, shapes_size=shapes_size, resolution=resolution,
                                max_iter=max_iter, elitism_rate=elitism_rate, mutation_rate=mutation_rate)
    resolver.resolve()
