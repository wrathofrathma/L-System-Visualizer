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
    """
    This class manages the 3D pyqtgraph widget used to display the MeshObjects of the lsystem.

    Attributes:
    mesh (MeshObject): The combined mesh that's actually displayed.
    mesh_positions (list): A list tracking the positions of each mesh, used in calculating the position of the combined mesh.
    original_fov (vec3): Field of view at initialization, used for resetting the camera.
    original_distance (vec3): Distnace of the camera at initialization, used for resetting the camera.
    """
    def __init__(self):
        """
        Constructor of LSystem3DWidget class.
        """
        super(LSystem3DWidget, self).__init__()

        # Production scene objects.
        self.mesh = None
        self.mesh_positions = []
        self.original_fov = self.opts['fov']
        self.original_distance = self.opts['distance']

    def reset_camera(self):
        """
        Resets the camera to the initial position & zoom level.
        """
        self.reset_zoom()

    def reset_zoom(self):
        """
        Resets the zoom level of the camera.
        """
        self.opts['fov'] = self.original_fov
        self.opts['distance']=self.original_distance
        self.update()

    def screenshot(self, filename, pos):
        """
        Captures the view of the widget and saves it to a filename on disk.

        Parameters:
        filename (str): Filename to save to.
        pos (???): Nani the fuck is this shit?
        """
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


    def add_mesh(self, mesh_list: list):
        """
        Adds MeshObjects to the scene.

        Parameters:
        mesh_list (list): List of MeshObjects.
        """
        meshes = []
        for m in mesh_list:
          for mesh in m:
            self.mesh_positions.append(mesh.opts["position"])
            meshes.append(mesh)

        self.mesh = self.combine_meshes(meshes)
        self.addItem(self.mesh)
        self.center_mesh()


    def combine_meshes(self, mesh_list: list):
        """
        Combines all added MeshObjects to one singular mesh. This mimimizes OpenGL calls used underneath and makes working with the data easier.

        Parameters:
        mesh_list (list): List of MeshObjects

        Returns:
        MeshObject: Combination of the passed MeshObjects in mesh_list.
        """
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

    def center_mesh(self):
      """
      Centers the mesh on the origin for a better camera experience.
      """
      positions = np.array(self.mesh_positions)
      avg_x = np.average(positions[:, 0])
      avg_y = np.average(positions[:, 1])
      avg_z = np.average(positions[:, 2])
      center = (avg_x, avg_y, avg_z)
      self.mesh.set_position(self.mesh.opts["position"] - center)
