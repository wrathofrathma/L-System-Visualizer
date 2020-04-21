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
    """Interface to pyqtgraph's GLMeshItem that allows us to scale and rotate the vertices.
    Attributes:
      opts (dict): Dictionary containing majority of the class' variables. At one point this was necessary due to passing some kwargs to a parent class, but is now pointless.
            vertexes: Array of vertexes in world coordinates.
            model_verts: Array of vertexes in model coordinates
            indices: Indices of the faces.
            position: World position
            rot_vec: Current rotation in the vector form.
            rot_quat: Current rotation in quaternion form
            scale: Scale of the model
            smooth: I forget.
            computeNormals: Do we compute normals? Nah. No lighting no need.
            drawEdges: Do we draw edges?
            drawFaces: Do we draw faces?
            shader: Custom shader - Deprecated.
            color: Color of the mesh.
            edgeColor: Color of the edges of the mesh.
    """

    def __init__(self, vertexes=None, indices=None, *args, **kwds):
        """
        Constructor for the MeshObject class.

        Parameters:
        vertexes (list): List of vertices used in the mesh.
        indices (list): List of indices for the faces used in the mesh.
        rot_quat (glm.quat): Quaternion defining the rotation of the object.
        rot_vec (vec3): Vector3 defining the rotation of the object.
        scale (vec3): Scale factor for each axis of the object. Defaults to (1.0, 1.0, 1.0)
        position (vec3): Position of the object. Defaults to (0.0, 0.0, 0.0)
        """
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
        if(vertexes is not None):
            self.opts["vertexes"] = vertexes
        if(indices is not None):
            self.opts["indices"] = indices
            
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

    def get_vertices(self):
        """Returns an array of vertexes in world coordinates."""
        return self.opts["vertexes"]

    def get_faces(self):
        """Returns an array of face indices."""
        return self.opts["indices"]

    def __reduce__(self):
        """Necessary for pickling & deep copying"""

        return (MeshObject, (self.get_vertices(), self.get_faces()))

    def update_vertices(self):
        """Updates the world vertices with the current scale/translation/rotation."""
        model = self.generate_model_matrix()
        rotation = self.get_rotation()
        verts = deepcopy(self.opts["model_verts"])
        nverts = []
        for v in verts:
            nv = rotation.apply(v)
            nv = np.array(model * vec4(nv, 1.0))
            nv = nv[:3]
            nverts += [nv]

        self.opts["vertexes"] = np.array(nverts, dtype=np.float32)
        self.opts["meshdata"].setVertexes(self.opts["vertexes"])
        if self.opts["indices"] is not None:
            self.opts["meshdata"].setFaces(self.opts["indices"])
        self.setMeshData(meshdata=self.opts["meshdata"])

    def set_position(self, pos, update=True):
        """Sets the position and optionally triggers an update of the vertices.

        Parameters:
        pos (vec3): 3 dimensional vector representing the new position of the object.
        update (boolean): True/False for whether to update the graphics card. Useful for bulking together GPU changes instead of switching contexts a bunch.
        """
        super(MeshObject, self).set_position(pos)
        self.opts["position"] = pos
        if update:
            self.update_vertices()

    def set_rotation(self, o, update=True):
        """Sets the rotation and optionally triggers an update of the vertices.

        Parameters:
        o (vec3): Vector3 representing the new orientation/rotation of the object.
        update (boolean): True/False for whether to update the graphics card. Useful for bulking together GPU changes instead of switching contexts a bunch.
        """
        super(MeshObject, self).set_rotation(o)
        self.opts["rotation"] = o
        if update:
            self.update_vertices()

    def set_scale(self, s, update=True):
        """Sets the scale and optionally triggers an update of the vertices.

        Parameters:
        update (boolean): True/False for whether to update the graphics card. Useful for bulking together GPU changes instead of switching contexts a bunch.
        """
        super(MeshObject, self).set_scale(s)
        self.opts["scale"] = s
        if update:
            self.update_vertices()

    def set_vertexes(self, v, update=True):
        """Sets the array of vertexes and optionally triggers an update of the vertices.

        Parameters:
        v (list): List of vertices to use in the mesh.
        update (boolean): True/False for whether to update the graphics card. Useful for bulking together GPU changes instead of switching contexts a bunch.
        """
        if v is None:
            return
        # If these aren't floats, then there is an error in normal calculation
        self.opts["model_verts"] = np.array(v, dtype=np.float32)
        if update:
            self.update_vertices()

    def set_indices(self, i, update=True):
        """Sets the array of indices and optionally triggers an update of the vertices.

        Parameters:
        i (list): List of the vertex indices used to define the faces of the mesh.
        update (boolean): True/False for whether to update the graphics card. Useful for bulking together GPU changes instead of switching contexts a bunch.
        """
        if i is None:
            return
        self.opts["indices"] = np.array(i)
        if update:
            self.update_vertices()
