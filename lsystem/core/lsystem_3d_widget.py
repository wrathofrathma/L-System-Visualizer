"""This file handles the OpenGL Window actions"""
from time import time

# Other includes
import numpy as np
# Lsystem includes
from glm import vec3
# Python core includes
from PIL import Image
# PyQt5 includes
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from lsystem.graphics.square import Square
from pyqtgraph.opengl import GLLinePlotItem, GLMeshItem, GLViewWidget


class LSystem3DWidget(GLViewWidget):
    def __init__(self):
        super(LSystem3DWidget, self).__init__()
        self.start_time = time()

        # Production scene objects.
        self.mesh_list = []
        
        self.run_test()



    def run_test(self):
        # Testing
        self.add_mesh(Square(pos=(0, 0, 0)))
        self.add_mesh(Square(pos=(3, 0, 0)))
        self.add_mesh(Square(pos=(4, 0, 0)))
        self.add_mesh(Square(pos=(7, 0, 0)))


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

    def clear_graph(self):
        self.clear_meshes()

    def add_mesh(self, mesh):
        self.mesh_list.append(mesh)
        self.addItem(self.mesh_list[-1])

    def clear_meshes(self):
        for mesh in self.mesh_list:
            self.removeItem(mesh)
        self.mesh_list.clear()
