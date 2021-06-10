import numpy as np
import cv2
import copy
import numpy.random as rnd
from PIL import Image

from .AesteticFunctions import functions


class PSO:
    def __init__(self,
                 target_image,
                 max_iter=151,
                 height=128,
                 width=128,
                 imitating_factor=0.6,
                 wmax=0.9,
                 wmin=0.4,
                 c1=2,
                 c2=2,
                 imitating=False):

        self.target_image = target_image

        self.Width = width
        self.Height = height

        self.target_image = self.target_image.convert("HSV")  # moving to HSV color space

        self.initial_image = 255*np.ones((self.Width, self.Height, 3))
        self.target_image = np.asarray(self.target_image)

        self.h_initial, self.s_initial, self.v_initial = cv2.split(self.initial_image)
        self.h_target, self.s_target, self.v_target = cv2.split(self.target_image)

        self.imitating_factor = imitating_factor
        self.particlesNr = self.Width * self.Height
        self.bounds = [[0, self.Width], [0, self.Height], [0, 255], [0, 255], [0, 255]]
        self.imitating = imitating
        self.particles_history = []
        self.wmax = wmax
        self.wmin = wmin
        self.c1 = c1  # cognitive factor
        self.c2 = c2  # social factor
        self.max_iter = max_iter
        self.F1, self.F2, self.F3, p1, p2, p3 = construct_fitness()
        self.particle_pos, self.particle_pos_val, self.particle_velocity, self.local_best, self.particle_best = self.initiation()
        self.r_w = np.random.random()  # factor for calculating w

    def fitness(self, x1, x2, x):
        """
        :param x1: x position in image
        :param x2: y position in image
        :param x: hsv vector
        :return: fitness
        """
        xh, xs, xv = x[0], x[1], x[2]
        x1, x2 = int(x1), int(x2)
        fh = abs(xh - self.F1(x1, x2))
        fs = abs(xs - self.F2(x1, x2))
        fv = abs(xv - self.F3(x1, x2))

        f = fh + fs + fv

        if self.imitating:
            ft = (abs(xh - self.h_target[x1][x2]) + abs(xs - self.s_target[x1][x2]) + abs(xv - self.v_target[x1][x2]))
            f = (1 - self.imitating_factor) * f + self.imitating_factor * ft
        return f

    def within_bounds(self, particle_pos):
        """
            DESCRIPTION:
                Checks whether a particle's position is within the bounds of the problem
                and constraints particles within bounds

            INPUTS:
            bounds      :bounds of problem in form [[x1,x2],[x3,x4]...]
            particle_pos:coordinates of a particle e.g [p1,p2,p3...]
        """
        for i in range(2, len(self.bounds)):
            t = i - 2
            if particle_pos[t] < self.bounds[i][0]:  # if particle is less than lower bound
                particle_pos[t] = self.bounds[i][0]
            elif particle_pos[t] > self.bounds[i][1]:  # if particle is more than higher bound
                particle_pos[t] = self.bounds[i][1]
        return

    def initiation(self):
        """
           OUTPUTS
           particle_pos      :array of random particle positions
           particle_best     :array of best particle positions (same as current)
           swarm_best        :coordinates of particle with best known position
           particle_velocity :array of random particle velocity arrays
           local_best        :array of the best particle in each neighbourhood
           local_best_fitness:function value evaluated at each local best
           particle_pos_val  :fitness of each particle

        """
        dimension = 3  # founding the number of dimensions
        particle_pos = np.zeros((self.Width, self.Height, 3))
        particle_velocity = np.zeros((self.Width, self.Height, 3))  # empty velocity matrix
        particle_pos_val = np.zeros((self.Width, self.Height))  # empty value matrix

        if self.imitating:
            self.distance_matrix = [[np.ones((self.Height, self.Width))] * self.Height] * self.Width

        for i in range(self.Height):
            for j in range(self.Width):
                x = [self.h_initial[i][j], self.s_initial[i][j], self.v_initial[i][j]]
                particle_pos[i][j] = x
                particle_pos_val[i][j] = self.fitness(i, j, particle_pos[i][j])
                particle_velocity[i][j] = [
                    rnd.randint(-abs(self.bounds[d][1] - self.bounds[d][0]), abs(self.bounds[d][1] - self.bounds[d][0]))
                    for d in range(2, dimension + 2)]

        local_best = local_best_get(particle_pos, particle_pos_val, self.Width, self.Height)

        particle_best = copy.deepcopy(particle_pos)  # setting all particles current positions to best

        return particle_pos, particle_pos_val, particle_velocity, local_best, particle_best

    def step(self, iter_count):
        w = self.wmax - (iter_count / self.max_iter) * (self.wmax - self.wmin) #+ self.r_w

        rp, rg = rnd.uniform(0, 1, 2)

        for i in range(self.Width):
            for j in range(self.Height):
                self.particle_velocity[i][j] = w * self.particle_velocity[i][j] \
                                          + (self.c1 * rp * (self.particle_best[i][j] - self.particle_pos[i][j])) \
                                          + (self.c2 * rg * (self.local_best[i][j] - self.particle_pos[i][j]))

                self.particle_pos[i][j] += self.particle_velocity[i][j]  # updating position

                self.within_bounds(self.particle_pos[i][j])

                particle_fitness = self.fitness(i, j, self.particle_pos[i][j])

                # updating the fitness of a particle
                if particle_fitness < self.particle_pos_val[i][j]:
                    self.particle_best[i][j][:] = self.particle_pos[i][j][:]  # updating personal best
                    self.particle_pos_val[i][j] = particle_fitness  # updating personal fitness

        self.local_best = copy.copy(local_best_get(self.particle_pos, self.particle_pos_val, self.Width,
                                    self.Height))  # calculating new local bests

        return np.array(copy.copy(self.particle_pos), np.uint8)


def construct_fitness():
    p1 = np.random.randint(14)
    p2 = np.random.randint(14)
    p3 = np.random.randint(14)
    print('We choose functions: ' + str(p1 + 1) + ' ' + str(p2 + 1) + ' ' + str(p3 + 1) + ' ')
    return functions[p1], functions[p2], functions[p3], p1, p2, p3


def local_best_get(particle_pos, particle_pos_val, w, h):
    # using von Neumann neighbourhood
    local_best = np.zeros((w, h, 3))  # creating empty local best list
    r = 1

    for i in range(r, w - r):
        for j in range(r, h - r):
            neighbours_positions = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                                    (i, j - 1), (i, j + 1),
                                    (i + 1, j), (i + 1, j), (i + 1, j + 1), ]

            local_values = [particle_pos_val[pos[0]][pos[1]] for pos in neighbours_positions]
            x, y = neighbours_positions[int(np.argmin(local_values))]
            local_best[i][j] = copy.deepcopy(particle_pos[x][y])

    return local_best