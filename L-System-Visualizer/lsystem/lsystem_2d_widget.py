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

from pyqtgraph import PlotWidget, GraphItem
from pyqtgraph.opengl import GLViewWidget, GLMeshItem, GLLinePlotItem

# Lsystem includes
from glm import vec3

# from graphics.graph_mesh import GraphObject
from lsystem.graph import Graph

# Other includes
import numpy as np

# class LSystemDisplayWidget(GLViewWidget):
# class LSystemDisplayWidget(MatplotlibWidget):
class LSystem2DWidget(PlotWidget):
    def __init__(self):
        super(LSystem2DWidget, self).__init__()
        self.start_time = time()

        # Production scene objects.
        self.graph = Graph()
        self.mesh = None

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

    def set_graph(self, graph):
        self.clear_graph()
        self.graph = graph
        (verts, adj) = self.graph.export_to_pyqtgraph()
        self.mesh = GraphItem()
        self.mesh.setData(pos=verts, adj=adj, symbol=None)
        self.addItem(self.mesh)

    def clear_graph(self):
        if isinstance(self.mesh, GraphItem):
            self.removeItem(self.mesh)
        self.mesh = None
