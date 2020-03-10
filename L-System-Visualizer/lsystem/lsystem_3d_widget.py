"""This file handles the OpenGL Window actions"""
# Python core includes
from PIL import Image
from time import time

# PyQt includes
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
)

from pyqtgraph.opengl import GLViewWidget, GLMeshItem, GLLinePlotItem

# Lsystem includes
from glm import vec3

# from graphics.graph_mesh import GraphObject
from lsystem.graph import Graph

# Other includes
import numpy as np

class LSystem3DWidget(GLViewWidget):
    def __init__(self):
        super(LSystem3DWidget, self).__init__()
        self.start_time = time()

        # Production scene objects.
        self.graph = Graph()
        self.mesh_list = []

    def reset_camera(self):
        pass

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def screenshot(self, filename):
        print("[ INFO ] Intentionally broken at the moment. There is a bug in pyqtgraph's image exporter so we'll need to fork or do it ourselves")

    def cleanup(self):
        pass

    def add_mesh(self, mesh):
        self.mesh_list.append(mesh)
        self.addItem(self.mesh_list[-1])

    def clear_meshes(self):
        for mesh in self.mesh_list:
            self.removeItem(mesh)
        self.mesh_list.clear()
