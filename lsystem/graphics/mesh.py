from copy import deepcopy
from math import degrees, pi, radians

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import PyQt5
from glm import vec3, vec4
from pyqtgraph.opengl import GLMeshItem, MeshData

from scipy.spatial.transform import Rotation as R
from lsystem.graphics.spatial_object import SpatialObject


class MeshObject(SpatialObject, GLMeshItem):
    """Interface to pyqtgraph's GLMeshItem that allows us to scale and rotate the vertices."""

    def __init__(self, **kwds):
        GLMeshItem.__init__(self)
        SpatialObject.__init__(self)
        # Argument extraction
        self.opts = {
            "vertexes": None,
            "model_verts": None,
            "indices": None,
            "position": vec3(0.0),
            "rot_vec": None,
            "rot_quat": None,
            "scale": vec3(1.0),
            "smooth": True,
            "computeNormals": False,
            "drawEdges": False,
            "drawFaces": True,
            "shader": None,
            "color": (1.0, 1.0, 1.0, 1.0),
            "edgeColor": (0.5, 0.5, 0.5, 1.0),
        }
        for k, v in kwds.items():
            self.opts[k] = v
            
        self.set_position(self.opts["position"], False)
        if (self.opts["rot_quat"] is not None):
          self.rotation = R.from_quat(self.opts["rot_quat"])
        if (self.opts["rot_vec"] is not None):
          self.rotation = R.from_rotvec(self.opts["rot_vec"])
        self.set_scale(self.opts["scale"], False)
        self.opts["meshdata"] = MeshData()
        self.set_vertexes(self.opts["vertexes"], False)
        self.set_indices(self.opts["indices"], False)
        if (self.opts["vertexes"] is not None):
            self.update_vertices()

    # TODO - Override all of the translation/rotation/scaling functions
    # and hook them into updating the mesh

    def get_vertices(self):
        return self.opts["vertexes"]

    def get_faces(self):
        return self.opts["indices"]

    # updates vertices with our scale/translation/rotation
    def update_vertices(self):
        # TODO - Actually do what i said this function will do
        model = self.generate_model_matrix()
        rotation = self.get_rotation()
        verts = deepcopy(self.opts["model_verts"])
        nverts = []
        for v in verts:
            nv = rotation.apply(v)
            nv = np.array(model * vec4(nv, 1.0))
            nv = nv[:3]
            nverts += [nv]

        # for v in verts:
        # nverts += [np.array((model * vec4(v, 1.0).xyz)), dtype = np.float32)]
        self.opts["vertexes"] = np.array(nverts, dtype=np.float32)
        self.opts["meshdata"].setVertexes(self.opts["vertexes"])
        if self.opts["indices"] is not None:
            self.opts["meshdata"].setFaces(self.opts["indices"])
        self.setMeshData(meshdata=self.opts["meshdata"])

    # def translate(self, v, update=True):
        # super(SpatialObject, self).translate(v)
        # if update:
            # self.update_vertices()

    # def rotate(self, rotation, update=True):
        # super(SpatialObject, self).rotate(rotation)
        # if update:
            # self.update_vertices()

    # def scale(self, s, update=True):
        # super(SpatialObject, self).scale(s)
        # if update:
            # self.update_vertices()

    def set_position(self, pos, update=True):
        super(MeshObject, self).set_position(pos)
        self.opts["position"] = pos
        if update:
            self.update_vertices()

    def set_rotation(self, o, update=True):
        super(MeshObject, self).set_rotation(o)
        self.opts["rotation"] = o
        if update:
            self.update_vertices()

    def set_scale(self, s, update=True):
        super(MeshObject, self).set_scale(s)
        self.opts["scale"] = s
        if update:
            self.update_vertices()

    def set_vertexes(self, v, update=True):
        if v is None:
            return
        # If these aren't floats, then there is an error in normal calculation
        self.opts["model_verts"] = np.array(v, dtype=np.float32)
        if update:
            self.update_vertices()

    def set_indices(self, i, update=True):
        if i is None:
            return
        self.opts["indices"] = np.array(i)
        if update:
            self.update_vertices()


if __name__ == "__main__":
    pg.mkQApp()
    view = gl.GLViewWidget()
    view.show()
    v = np.array([(0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0)])
    f = np.array([[0, 1, 2], [1, 2, 3]])
    # f = np.array([[0, 1, 2, 1, 2, 3]])
    # f = np.array([[1, 2, 3]])
    # f = None
    # f = np.array([[0, 1, 2]])
    # print(f)
    mesh = MeshObject(indices=f, vertexes=v)
    # m = MeshData()
    # m.setVertexes(v)
    # m.setFaces(f)
    # mesh = GLMeshItem(meshdata=m)
    view.addItem(mesh)
    mesh.set_position((0, 1, 0))
    # mesh.set_rotation((np.sin(pi / 2), 0, 0))
    # mesh.set_rotation((0, -pi / 2, 0))
    mesh.set_rotation((0, radians(90), 0))
    # mesh.rotate((0, radians(90), 0))
    mesh.set_scale(vec3(2.0))
    xgrid = gl.GLGridItem()
    ygrid = gl.GLGridItem()
    zgrid = gl.GLGridItem()
    view.addItem(xgrid)
    view.addItem(ygrid)
    view.addItem(zgrid)

    xgrid.rotate(90, 0, 1, 0)
    ygrid.rotate(90, 1, 0, 0)

    xgrid.scale(0.2, 0.1, 0.1)
    ygrid.scale(0.2, 0.1, 0.1)
    zgrid.scale(0.1, 0.2, 0.1)
    print(mesh.get_vertices())
    import sys
    from pyqtgraph import QtCore

    if sys.flags.interactive != 1 or not hasattr(QtCore, "PYQT_VERSION"):
        pg.QtGui.QApplication.exec()
