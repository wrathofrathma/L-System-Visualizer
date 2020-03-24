# This file is for our undirected graph class and helper functions.
# A few notes on the different design decisions here.
# 1. Using a python dictionary with vertices as a key lets us check if vertices exist in much quicker time than doing some_list.index(value).
# 2. Using tuples for vertices allows them to be hashable, aka used as keys in a dict.
# 3. By storing each edge between v1&v2 only once in v1's adjacency_list, we avoid any possible concurrency issues.
# 4. I'm pretty sure we avoid global interpreter lock with this implementation of threading. Will need thorough testing.
from time import time

import numpy as np

from lsystem.graphics.colors import Colors


class Graph:
    def __init__(self):
        # Vertices will be a dictionary that stores an adjacency list for each vertex.
        self.adjacency_list = {}
        self.colors = []
        self.vertices = []
        self.n = 0

    # Let's assume the vertex passed is a tuple since that's hashable and we need that for dictionaries to work.
    # Optional color passed for each vertex. Default is white.
    def add_vertex(self, vertex, color=Colors.white):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {"edges": [], "color": color, "index": self.n}
            self.vertices.append(vertex)
            self.colors.append(color)
            self.n += 1

    # Assume both v1 and v2 are tuples of form (x,y,z)
    # We'll just add to v1 each time.
    def add_edge(self, v1, v2):
        if v1 not in self.adjacency_list:
            self.add_vertex(v1)
        if v2 not in self.adjacency_list:
            self.add_vertex(v2)
        if not self.edge_exists(v1, v2):
            self.adjacency_list[v1]["edges"].append(v2)

    def clear(self):
        self.adjacency_list = {}
        self.colors = []
        self.vertices = []

    # Checks if an edge exists.
    def edge_exists(self, v1, v2):
        if (
            v1 in self.adjacency_list[v2]["edges"]
            or v2 in self.adjacency_list[v1]["edges"]
        ):
            return True
        return False

    def export_to_ogl_verts(self):
        verts = []
        for v in self.vertices:
            for e in self.adjacency_list[v]["edges"]:
                verts += [v, e]
        return np.array(verts)

    def export_to_matplot2d(self):
        lines = []
        for v in self.vertices:
          for e in self.adjacency_list[v]["edges"]:
            lines += [((v[0], e[0]), (v[1], e[1]))]
        return lines

    def export_to_pyqtgraph(self):
        # Reshape in case we have 3 dimensional data
        verts = np.array(self.vertices)
        verts = verts[:, :2]
        adj = []
        for v in self.vertices:
          for e in self.adjacency_list[v]["edges"]:
            adj += [(self.adjacency_list[v]["index"], self.adjacency_list[e]["index"])]
        adj = np.array(adj)
        return (verts, adj)

    def generate_indices(self, adjacency_list, vert_list):
        # for each vertice in our vertice range
        #   for every outgoing edge
        #       add that line's indice.
        start = time()
        inds = []
        for v in vert_list:
            for e in adjacency_list[v]["edges"]:
                inds += [adjacency_list[v]["index"], adjacency_list[e]["index"]]
        end = time()
        print(
            "[ INFO ] Finished exporting to OGL indices in "
            + str(round(end - start, 3))
            + "s"
        )
        return inds

    # this function will generate opengl vertex data from a graph.
    def export_to_ogl_indices(self):
        adjacency_list = self.adjacency_list
        vertices = np.array(self.vertices)
        colors = self.colors
        indices = self.generate_indices(adjacency_list, self.vertices)
        vertices = vertices.reshape(vertices.shape[0] * vertices.shape[1])
        return (np.array(vertices), np.array([0, 0, 0, 1]), np.array(indices))
