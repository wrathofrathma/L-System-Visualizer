"""This file handles the OpenGL Window actions"""
from time import time

# Other includes
import numpy as np
# Lsystem includes
from glm import vec3
# Python core includes
from PIL import Image
from pyqtgraph import GraphItem, PlotWidget
from pyqtgraph.opengl import GLLinePlotItem, GLMeshItem, GLViewWidget
# PyQt5 includes
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

# from graphics.graph_mesh import GraphObject
from lsystem.core.graph import Graph

import pyscreenshot as ImageGrab

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
    def reset_zoom(self):
        self.autoRange()
    def screenshot(self, filename,pos):
        #print("[ INFO ] Intentionally broken at the moment. There is a bug in pyqtgraph's image exporter so we'll need to fork or do it ourselves")
        #rect is the rectange (x,y,width,height) of the widget
        rect = self.frameGeometry()
        #shift over to get absl. pos
        rect.translate(pos)
        im = ImageGrab.grab(bbox=(rect.x(), rect.y(), rect.x()+rect.width(), rect.y()+rect.height())) # X1,Y1,X2,Y2
        im.save(filename)

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
