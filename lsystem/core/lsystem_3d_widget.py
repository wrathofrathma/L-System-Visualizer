"""This file handles the OpenGL Window actions"""
from time import time
import math
# Other includes
import numpy as np
# Lsystem includes
from glm import vec3
# Python core includes
from PIL import Image
# PyQt5 includes
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from lsystem.graphics.mesh import MeshObject

from pyqtgraph.opengl import GLLinePlotItem, GLMeshItem, GLViewWidget


class LSystem3DWidget(GLViewWidget):
    def __init__(self):
        super(LSystem3DWidget, self).__init__()
        self.start_time = time()

        # Production scene objects.
        self.mesh = None
        self.mesh_positions = []
        self.original_fov = self.opts['fov']
        self.original_distance = self.opts['distance']

    def reset_camera(self):
        pass

    def reset_zoom(self):
        self.opts['fov'] = self.original_fov
        self.opts['distance']=self.original_distance
        self.update()

    def screenshot(self, filename, pos):
        #print("[ INFO ] Intentionally broken at the moment. There is a bug in pyqtgraph's image exporter so we'll need to fork or do it ourselves")
        #rect is the rectange (x,y,width,height) of the widget
        # rect = self.frameGeometry()
        # #shift over to get absl. pos
        # rect.translate(pos)
        # im = ImageGrab.grab(bbox=(rect.x(), rect.y(), rect.x()+rect.width(), rect.y()+rect.height())) # X1,Y1,X2,Y2
        # im.save(filename)
        self.grabFrameBuffer().save(filename)
        # self.renderPixmap().save(filename)

    def clear(self):
        """Removes all mesh objects from the scene."""
        self.mesh_positions.clear()
        if(self.mesh is not None):
            self.removeItem(self.mesh)


    def add_mesh(self, mesh_list):
        """Sets the mesh of the scene to a combination of the list of meshes passed."""
        meshes = []
        for m in mesh_list:
          for mesh in m:
            self.mesh_positions.append(mesh.opts["position"])
            meshes.append(mesh)

        self.mesh = self.combine_meshes(meshes)
        self.addItem(self.mesh)
        self.center_meshes()


    def combine_meshes(self, mesh_list: list):
        """Combines mesh list into a singular mesh"""
        # So can't we do this by tracking the offset of the vert list when we add the vertexes
        # Then when we add the faces we just add the offset to each face?
        verts = np.array([])
        faces = np.array([])
        for mesh in mesh_list:
            offset = len(verts)
            verts = np.append(verts, mesh.opts["vertexes"])
            faces = np.append(faces, mesh.opts["indices"] + offset)
            verts = verts.reshape(math.floor(verts.shape[0]/3),3)
            faces = faces.reshape(math.floor(faces.shape[0]/3),3)
        faces = faces.astype(int)
        return MeshObject(vertexes=verts, indices=faces)

    def center_meshes(self):
      """Centers the entire mesh list on the origin"""
      positions = np.array(self.mesh_positions)
      # print(positions.shape)
      avg_x = np.average(positions[:, 0])
      avg_y = np.average(positions[:, 1])
      avg_z = np.average(positions[:, 2])
      center = (avg_x, avg_y, avg_z)
      self.mesh.set_position(self.mesh.opts["position"] - center)
