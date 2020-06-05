import numpy as np
import random
import matplotlib.pyplot as plt
import math
from typing import Set, Tuple, List
import time
from matplotlib.animation import FuncAnimation


class Point:
    def __init__(self, i, points_num, coord=None):
        self.i = i
        self.points_num = points_num
        self.coord = (random.random(), random.random()) if coord is None else coord

    def x(self):
        return self.coord[0]

    def y(self):
        return self.coord[1]

    def dist(self, p):  # not euclidean distance
        return np.sum([(i - j) ** 2 for i, j in zip(p.coord, self.coord)])

    def __str__(self):
        return f"Point {self.i}: {self.coord}"


class ConnectedGraph:
    def __init__(self, points_coord=None, points_num=0):
        if points_coord is None:
            self.points_coord = random_points(points_num)
        else:
            points_num = len(points_coord)
            self.points_coord = points_coord
        self.points: List[Point] = [Point(i, points_num, coord) for i, coord in enumerate(self.points_coord)]
        self.points_num = points_num
        self.distances = np.array([[p1.dist(p2) for p2 in self.points] for p1 in self.points])

    def add_point(self, coord: tuple):
        self.points.append(Point(self.points_num, self.points_num, coord))
        self.points_coord = np.vstack((self.points_coord, coord))
        for p in self.points:
            print(p.points_num)
            p.points_num += 1
        self.points_num += 1
        self.distances = np.array([[p1.dist(p2) for p2 in self.points] for p1 in self.points])

    def rand_p(self):
        return self.points[random.randint(0, self.points_num - 1)]

    def get_p(self, ind):
        return self.points[ind]

    def show_graph(self):
        px = self.points_coord.T[0]
        py = self.points_coord.T[1]
        plt.scatter(px, py)
        plt.show()


class TspSimAnn:
    def __init__(self, g: ConnectedGraph, t=10, alpha=0.99):
        self.g = g
        self.points_num = g.points_num
        self.path = np.arange(g.points_num, dtype=int)
        self.curr_path_w = self.get_path_w(self.path)
        self.t = t
        self.alpha = alpha
        self.switch_prob = 1

    def animate(self):
        pass

    def step(self):
        p1, p2 = random.randint(0, self.points_num - 1), random.randint(0, self.points_num - 1)
        self.path[p1], self.path[p2] = self.path[p2], self.path[p1]
        new_w = self.get_path_w(self.path)

        self.switch_prob = self.prob_of_switch(new_w)
        if self.switch_prob > random.random():
            self.curr_path_w = new_w
        else:
            self.path[p1], self.path[p2] = self.path[p2], self.path[p1]
        self.t *= self.alpha

    def prob_of_switch(self, new_w):
        if new_w < self.curr_path_w:
            return 1
        return math.exp((self.curr_path_w - new_w) / self.t)

    def get_path_w(self, path):
        w = 0
        prev_i = path[-1]
        for i in path:
            w += self.g.distances[i, prev_i]
            prev_i = i
        return w

    def get_connections_data(self):
        cx = [self.g.points_coord[i][0] for i in self.path]
        cx.append(self.g.points_coord[self.path[0]][0])

        cy = [self.g.points_coord[i][1] for i in self.path]
        cy.append(self.g.points_coord[self.path[0]][1])
        return cx, cy

    def show_path(self):
        px = self.g.points_coord.T[0]
        py = self.g.points_coord.T[1]
        cx, cy = self.get_connections_data()

        plt.scatter(px, py)
        plt.plot(cx, cy)
        plt.show()


def random_points(points_num):
    shape = (points_num, 2)
    return np.random.random(shape)


def main():
    p_num = 10
    g = ConnectedGraph(p_num)
    t = TspSimAnn(g, t=2 * p_num)

    fig, ax = plt.subplots()

    px = t.g.points_coord.T[0]
    py = t.g.points_coord.T[1]

    plt.scatter(px, py)
    ln, = plt.plot([], [])

    def update(frame):
        cx, cy = t.get_connections_data()
        ln.set_data(cx, cy)
        t.step()
        return ln,

    steps = 1000

    ani = FuncAnimation(fig, update, save_count=1, frames=steps, repeat=False, interval=20)
    plt.show()
    # t.show_path()
    # g.show_graph()


if __name__ == '__main__':
    main()
