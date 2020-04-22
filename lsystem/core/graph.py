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
    """
    This class is an undirected graph implementation with utility methods for exporting to different mesh formats.

    Attributes:
    adjacency_list (dict): Dictionary of vertices and their connected partners.
    colors (list): List of vertex colors.
    vertices (list): List of vertices.
    """
    def __init__(self):
        """
        Constructor for the Graph class.
        """
        # Vertices will be a dictionary that stores an adjacency list for each vertex.
        self.adjacency_list = {}
        self.colors = []
        self.vertices = []
        self.n = 0

    # Let's assume the vertex passed is a tuple since that's hashable and we need that for dictionaries to work.
    # Optional color passed for each vertex. Default is white.
    def add_vertex(self, vertex, color=Colors.white):
        """
        Adds a vertex to the undirected graph.

        Parameters:
        vertex (vec3): Vertex to add.
        color (vec3): Color of the vertex.
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {"edges": [], "color": color, "index": self.n}
            self.vertices.append(vertex)
            self.colors.append(color)
            self.n += 1

    # Assume both v1 and v2 are tuples of form (x,y,z)
    # We'll just add to v1 each time.
    def add_edge(self, v1, v2):
        """
        Adds an edge between two vertices. Will add the vertices if they don't already exist in the graph.

        Parameters:
        v1 (vec3): Vertex position 1
        v2 (vec3): Vertex position 2
        """
        if v1 not in self.adjacency_list:
            self.add_vertex(v1)
        if v2 not in self.adjacency_list:
            self.add_vertex(v2)
        if not self.edge_exists(v1, v2):
            self.adjacency_list[v1]["edges"].append(v2)

    def clear(self):
        """
        Clears the graph.
        """
        self.adjacency_list = {}
        self.colors = []
        self.vertices = []

    # Checks if an edge exists.
    def edge_exists(self, v1, v2):
        """
        Checks if an edge exists between two vertices.

        Parameters:
        v1 (vec3): Vertex 1
        v2 (vec3): Vertex 2

        Returns:
        - True/False for if it exists.
        """
        if (
            v1 in self.adjacency_list[v2]["edges"]
            or v2 in self.adjacency_list[v1]["edges"]
        ):
            return True
        return False

    def export_to_ogl_verts(self):
        """
        Exports the graph vertices to a format OpenGL can use.

        Returns:
        - numpy.array: A numpy array of the vertices.
        """
        verts = []
        for v in self.vertices:
            for e in self.adjacency_list[v]["edges"]:
                verts += [v, e]
        return np.array(verts)

    def export_to_matplot2d(self):
        """
        Exports the graph to vertices matplotlib can use.

        Returns:
        - list: List of vertices.
        """
        lines = []
        for v in self.vertices:
          for e in self.adjacency_list[v]["edges"]:
            lines += [((v[0], e[0]), (v[1], e[1]))]
        return lines

    def export_to_pyqtgraph(self):
        """
        Exports the graph to a format MeshObject can use for pyqtgraph's 3D mesh objects.

        Returns:
        - tuple: (verts, adj)
        """
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
        """
        Generates the indices of the vertices/adjacency list for OpenGL element drawing calls.

        Parameters:
        adjacency_list (dict): Dictionary of vertex->vertex mappings
        vert_list (list): List of all vertices.

        Returns:
        - list: List of indices.
        """
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
        """
        Generates & exports all vertex, color, and indice data needed for OpenGL Element drawing calls.

        Returns:
        - tuple(np.array, np.array, np.array)
        - - Array 0 is the array of vertices.
        - - Array 1 is the array of colors.
        - - Array 2 is the array of indices.
        """
        adjacency_list = self.adjacency_list
        vertices = np.array(self.vertices)
        colors = self.colors
        indices = self.generate_indices(adjacency_list, self.vertices)
        vertices = vertices.reshape(vertices.shape[0] * vertices.shape[1])
        return (np.array(vertices), np.array([0, 0, 0, 1]), np.array(indices))
