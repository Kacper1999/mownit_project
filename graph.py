import numpy as np
import random
import matplotlib.pyplot as plt

from typing import Set, Tuple, List


class Node:
    def __init__(self, i, coord=None):
        self.i = i
        self.coord = (random.random(), random.random()) if coord is None else coord
        self.connections = set()

    def x(self):
        return self.coord[0]

    def y(self):
        return self.coord[1]

    def add_connection(self, to):
        self.connections.add(to)

    def __str__(self):
        return str(self.coord)


class Graph:
    def __init__(self, points_num=0, connections_num=None):
        self.points_coord = random_points(points_num)
        self.points: List[Node] = [Node(i, coord) for i, coord in enumerate(self.points_coord)]
        self.points_num = points_num
        self.connections: Set[Tuple[Node, Node]] = set()
        if connections_num is not None:
            self.add_random_connections(connections_num)

    def add_point(self, coord: tuple):
        self.points.append(Node(self.points_num, coord))
        self.points_coord = np.vstack((self.points_coord, coord))
        self.points_num += 1

    def can_add_connection(self, p1: Node, p2: Node):
        return not (p1 == p2 or (p1, p2) in self.connections or (p2, p1) in self.connections)

    def add_connection(self, p1: Node, p2: Node):
        if not self.can_add_connection(p1, p2):
            print("Connection already exists or trying to connect to itself")
            return False
        p1.add_connection(p2)
        p2.add_connection(p1)
        self.connections.add((p1, p2))
        return True

    def rand_p(self):
        return self.points[random.randint(0, self.points_num - 1)]

    def get_p(self, ind):
        return self.points[ind]

    def get_new_connection(self):
        p1, p2 = self.rand_p(), self.rand_p()
        while not self.can_add_connection(p1, p2):
            p1, p2 = self.rand_p(), self.rand_p()
        return p1, p2

    def add_random_connections(self, connections_num):
        for _ in range(connections_num):
            p1, p2 = self.get_new_connection()
            self.add_connection(p1, p2)

    def show_graph(self):
        px = self.points_coord.T[0]
        py = self.points_coord.T[1]
        plt.scatter(px, py)
        for connection in self.connections:
            cx = [point.x() for point in connection]
            cy = [point.y() for point in connection]
            plt.plot(cx, cy, "r")
        plt.show()

    def is_connected(self):
        return sum(1 for _ in self.bfs()) == self.points_num

    def bfs(self):
        visited = np.full(self.points_num, False, dtype=bool)
        q = [self.points[0]]
        visited[0] = True
        while q:
            point = q.pop(0)
            yield point
            for c in point.connections:
                if not visited[c.i]:
                    visited[c.i] = True
                    q.append(c)


def random_points(points_num):
    shape = (points_num, 2)
    return np.random.random(shape)


def main():
    p_num = 8
    g = Graph(p_num, p_num)
    print(g.is_connected())
    g.show_graph()


if __name__ == '__main__':
    main()
