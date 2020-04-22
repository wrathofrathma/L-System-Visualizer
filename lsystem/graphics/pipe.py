import numpy as np
import math
from glm import vec3
import glm

from lsystem.graphics.mesh import MeshObject
from scipy.spatial.transform import Rotation as R

class Pipe(MeshObject):
  def __init__(self, start: vec3 = None, end: vec3 = None, rotation=vec3(0.0)):
    pos = np.multiply(np.add(start,end),.5)
    up = vec3(0,1,0)
    if(vec3(end-start) != up and vec3(end-start) != up*-1):
      rotation = glm.quatLookAt(vec3(end-start), up)
      MeshObject.__init__(self, position=pos, rot_quat=rotation)
    else:
      up = vec3(0,0,1)
      rotation = glm.quatLookAt(vec3(end-start), up)
      MeshObject.__init__(self, position=pos, rot_quat=rotation)


     
    verts = np.array([(0, 0, -0.5), (0, 0, 0.5), (0.1, 0.0, 0.5), (0.07071067811865477, 0.07071067811865475, 0.5), (6.123233995736766e-18, 0.1, 0.5), (-0.07071067811865475, 0.07071067811865477, 0.5), (-0.1, 1.2246467991473533e-17, 0.5), (-0.07071067811865477, -0.07071067811865475, 0.5), (-1.8369701987210297e-17, -0.1, 0.5), (0.07071067811865474, -0.07071067811865477, 0.5), (0.1, 0.0, -0.5), (0.07071067811865477, 0.07071067811865475, -0.5), (6.123233995736766e-18, 0.1, -0.5), (-0.07071067811865475, 0.07071067811865477, -0.5), (-0.1, 1.2246467991473533e-17, -0.5), (-0.07071067811865477, -0.07071067811865475, -0.5), (-1.8369701987210297e-17, -0.1, -0.5), (0.07071067811865474, -0.07071067811865477, -0.5)]
)
    faces = np.array([(0, 9, 2), (1, 17, 10), (0, 2, 3), (1, 10, 11), (0, 3, 4), (1, 11, 12), (0, 4, 5), (1, 12, 13), (0, 5, 6), (1, 13, 14), (0, 6, 7), (1, 14, 15), (0, 7, 8), (1, 15, 16), (0, 8, 9), (1, 16, 17), (17, 2, 9), (17, 10, 2), (10, 3, 2), (10, 11, 3), (11, 4, 3), (11, 12, 4), (12, 5, 4), (12, 13, 5), (13, 6, 5), (13, 14, 6), (14, 7, 6), (14, 15, 7), (15, 8, 7), (15, 16, 8), (16, 9, 8), (16, 17, 9)]
)
    self.set_vertexes(np.array(verts), False)
    self.set_indices(np.array(faces))
    self.start = start
    self.end = end

  def __reduce__(self):
    """Reduction code allowing us to pickle this class, thus allowing it to be deepcopied"""
    return (Pipe, (self.start, self.end))


  def _gen_pipe(self):
    """Function I used to create the verts for our pipe. I dumped these to a file to hardcode them to save runtime costs."""
    self.radius = 0.1
    self.divs = 8
    # self.height = 3 * self.radius
    self.height = 1

    # Generate circles for top and bottom of the pipe
    bcircle = []
    tcircle = []
    cstep = 2 * np.pi / self.divs
    for d in range(self.divs):
      v = (self.radius * math.cos(d * cstep), self.radius * math.sin(d * cstep))
      bcircle.append((v[0], v[1], self.height / 2.0))
      tcircle.append((v[0], v[1], -self.height / 2.0))

    # Origins Bottom      Top
    verts = [(0, 0, -self.height / 2.0), (0, 0, self.height / 2.0)]
    verts += (bcircle)
    verts += (tcircle)
    # Create circle faces from the individual circles.
    faces = []
    bcircle_range = np.arange(2, 2 + len(bcircle))
    tcircle_range = np.arange(2 + len(bcircle), 2 + len(bcircle) + len(tcircle))
    for i in range(self.divs):
      bf = (0, bcircle_range[i - 1], bcircle_range[i])
      tf = (1, tcircle_range[i - 1], tcircle_range[i])
      faces.append(bf)
      faces.append(tf)
    # Now that circle faces are complete, let's make the individual faces between them.
    # We can do this by iterating through both top & bottom circles 2 verts at a time
    # and creating a divided square.

    for i in range(self.divs):
      tl = tcircle_range[i - 1]
      tr = tcircle_range[i]
      bl = bcircle_range[i-1]
      br = bcircle_range[i]
      faces.append((tl, br, bl))
      faces.append((tl, tr, br))
    print(verts)
    print("")
    print(faces)

if __name__=="__main__":
  p = Pipe()
