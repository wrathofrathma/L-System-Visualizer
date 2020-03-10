from graphics.mesh import MeshObject
from glm import vec3
import numpy as np

class Square(MeshObject):
    """afjaksdflhas"""

    def __init__(self, pos=vec3(0.0), rotation=vec3(0.0)):
        MeshObject.__init__(self, position=pos, rotation=rotation)
        self.set_vertexes(np.array([
          (0.0, 0.0, 0.0),
          (0.0, 1.0, 0.0),
          (1.0, 0.0, 0.0),
          (1.0, 1.0, 0.0)
          ]), False)
        self.set_indices(np.array([[0, 1, 2], [1, 2, 3]]))
        

if __name__ == "__main__":
    m = Square()
