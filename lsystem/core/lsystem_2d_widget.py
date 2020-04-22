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

class LSystem2DWidget(PlotWidget):
    """
    This class manages the 2D PlotWidet used to display the lsystem.

    Attributes:
    mesh (MeshObject): The mesh object that is being displayed.
    graph (Graph): Digraph class used to minimize vector redundancy.
    """
    def __init__(self):
        """
        Constructor of the LSystem2DWidget
        """
        super(LSystem2DWidget, self).__init__()

        # Production scene objects.
        self.graph = Graph()
        self.mesh = None

    def reset_camera(self):
        """
        Resets the camera to the initial position & zoom level.
        """
        self.reset_zoom() # This happens to do the same thing.

    def reset_zoom(self):
        """
        Resets the camera to the initial position & zoom level.
        """
        self.autoRange()

    def screenshot(self, filename, pos):
        """
        Captures the view of the widget and saves it to a filename on disk.

        Parameters:
        filename (str): Filename to save to.
        pos (???): Nani the fuck is this shit?
        """
        #print("[ INFO ] Intentionally broken at the moment. There is a bug in pyqtgraph's image exporter so we'll need to fork or do it ourselves")
        #rect is the rectange (x,y,width,height) of the widget
        rect = self.frameGeometry()
        #shift over to get absl. pos
        rect.translate(pos)
        im = ImageGrab.grab(bbox=(rect.x(), rect.y(), rect.x()+rect.width(), rect.y()+rect.height())) # X1,Y1,X2,Y2
        im.save(filename)

    def set_graph(self, graph):
        """
        Sets the graph object the scene uses to generate the mesh.

        Parameters:
        graph (Graph): Digraph used to generate the mesh.
        """
        self.clear()
        self.graph = graph
        (verts, adj) = self.graph.export_to_pyqtgraph()
        self.mesh = GraphItem()
        self.mesh.setData(pos=verts, adj=adj, symbol=None)
        self.addItem(self.mesh)

    def clear(self):
        """
        Removes the mesh from the scene.
        """
        if isinstance(self.mesh, GraphItem):
            self.removeItem(self.mesh)
        self.mesh = None
