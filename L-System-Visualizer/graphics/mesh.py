# from graphics.SpatialObject import SpatialObject
from pyqtgraph.opengl import MeshData, GLMeshItem
import numpy as np
from glm import vec3

# Testing
from spatial_object import SpatialObject
import pyqtgraph as pg
import pyqtgraph.opengl as gl


class MeshObject(SpatialObject, GLMeshItem):
    """Interface to pyqtgraph's GLMeshItem that allows us to scale and rotate the vertices."""

    def __init__(self, **kwds):
        SpatialObject.__init__(self)
        GLMeshItem.__init__(self)
        # Argument extraction
        self.opts = {
            'vertexes': None,
            'indices': None,
            'position': vec3(0.0),
            'orientation': vec3(0.0),
            'scale': vec3(1.0),
            'smooth': True,
            'computeNormals': False,
            'drawEdges': False,
            'drawFaces': True,
            'shader': None,
            'color': (1., 1., 1., 1.),
            'edgeColor': (0.5, 0.5, 0.5, 1.0)
            }
        for k, v in kwds.items():
            self.opts[k] = v
        self.set_position(self.opts['position'], False)
        self.set_orientation(self.opts['orientation'], False)
        self.set_scale(self.opts['scale'], False)
        self.opts['meshdata'] = MeshData()
        self.set_vertexes(self.opts['vertexes'], False)
        self.set_indices(self.opts['indices'], False)
        self.updates_vertices()
    
    # TODO - Override all of the translation/rotation/scaling functions 
    # and hook them into updating the mesh

    # updates vertices with our scale/translation/rotation
    def updates_vertices(self):
        # TODO - Actually do what i said this function will do
        self.opts['meshdata'].setVertexes(self.opts['vertexes'])
        self.setMeshData(meshdata=self.opts['meshdata'])

    def set_position(self, pos, update=True):
        super(MeshObject, self).set_position(pos)
        self.opts['position'] = pos
        if(update):
            self.update_vertices()

    def set_orientation(self, o, update=True):
        super(MeshObject, self).set_orientation(o)
        self.opts['orientation'] = o
        if(update):
            self.update_vertices()

    def set_scale(self, s, update=True):
        super(MeshObject, self).set_scale(s)
        self.opts['scale'] = s
        if(update):
            self.update_vertices()

    def set_vertexes(self, v, update=True):
        if(v is None):
            return
        # If these aren't floats, then there is an error in normal calculation
        self.opts['vertexes'] = np.array(v, dtype=np.float32)
        if(update):
            self.update_vertices()

    def set_indices(self, i, update=True):
        if(i is None):
            return
        self.opts['indices'] = np.array(i)
        if(update):
            self.update_vertices()


if __name__ == "__main__":
    pg.mkQApp()
    view = gl.GLViewWidget()
    view.show()
    a = {}
    v = np.array([(0., 0., 0.), (0., 1., 0.), (1., 0., 0.), (1., 1., 1.)])
    f = np.array([[0, 1, 3]])
    # print(f)
    a['vertexes'] = v
    a['faces'] = f
    mesh = MeshObject(indices=f, vertexes=v)
    # m = MeshData()
    # m.setVertexes(v)
    # m.setFaces(f)
    # mesh = GLMeshItem(meshdata=m)
    view.addItem(mesh)
    xgrid = gl.GLGridItem()
    ygrid = gl.GLGridItem()
    zgrid = gl.GLGridItem()
    # view.addItem(xgrid)
    # view.addItem(ygrid)
    # view.addItem(zgrid)

    xgrid.rotate(90, 0, 1, 0)
    ygrid.rotate(90, 1, 0, 0)

    xgrid.scale(0.2, 0.1, 0.1)
    ygrid.scale(0.2, 0.1, 0.1)
    zgrid.scale(0.1, 0.2, 0.1)
    import sys
    from pyqtgraph import QtCore
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec()
