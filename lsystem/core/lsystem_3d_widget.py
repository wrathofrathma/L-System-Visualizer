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
        self.mesh_positions = []
        self.original_fov = self.opts['fov']
        self.original_distance = self.opts['distance']

    def reset_camera(self):
        pass

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def reset_zoom(self):
        self.opts['fov'] = self.original_fov
        self.opts['distance']=self.original_distance
        self.update()

    def screenshot(self, filename):
        print("[ INFO ] Intentionally broken at the moment. There is a bug in pyqtgraph's image exporter so we'll need to fork or do it ourselves")

    def cleanup(self):
        pass

    def clear_graph(self):
        self.clear_meshes()

    def add_mesh(self, mesh_list):
        for m in mesh_list:
          for mesh in m:
            self.mesh_positions.append(mesh.opts["position"])
            self.mesh_list.append(mesh)
            self.addItem(mesh)
        self.center_meshes()

    def clear_meshes(self):
        """Removes all mesh objects from the scene"""
        self.mesh_positions.clear()
        for mesh in self.mesh_list:
            self.removeItem(mesh)
        self.mesh_list.clear()

    def center_meshes(self):
      """Centers the entire mesh list on the origin"""
      positions = np.array(self.mesh_positions)
      # print(positions.shape)
      avg_x = np.average(positions[:, 0])
      avg_y = np.average(positions[:, 1])
      avg_z = np.average(positions[:, 2])
      center = (avg_x, avg_y, avg_z)
      for mesh in self.mesh_list:
        mesh.set_position(mesh.opts["position"] - center)
