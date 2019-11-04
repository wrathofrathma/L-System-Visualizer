from OpenGL.GL import *

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np
from lsystem.graphics.QuaternionObject import *
from glm import value_ptr
from ctypes import c_void_p

from lsystem.graphics.colors import Colors
from lsystem.graph import *
from lsystem.graphics.GraphMesh import GraphObject

# This class is a gridspace that overlays the l-system and detects intersections in individual gridspaces.
# It has n divisions across the X & Y axis.
class Grid2D(GraphObject):
    def __init__(self, divisions=10):
        super().__init__(2)
        # Grid specific code
        self.divisions = divisions
        # Boolean grid for flagging which grid spaces are intersected.
        self.grid=np.ndarray((divisions, divisions), dtype=np.bool)
        self.generate_vertices()

        # Translate & scale into our view. 
        self.translate([-0.5, 0, 0])
        self.scale(1.0/divisions)

    # Will generate vertices based on the number of divisions provided.
    # We're going to assume each box is composed of a 1x1 unit square then scale down later.
    # We'll be using GL_LINES, which take 2 floats per line.
    def generate_vertices(self):
        g = Graph()
        for x in range(0,self.divisions):
            for y in range(0,self.divisions):
                # Let's only insert each line once.
                # Bottom line is only inserted if y=0
                if(y==0):
                    g.add_edge((x,y),(x+1,y))
                    # self.vertices+=[x,y] # Bottom left
                    # self.vertices+=[x+1,y] # Bottom right 
                # Right line is inserted every time.
                g.add_edge((x+1,y),(x+1,y+1))
                # self.vertices+=[x+1,y] # Bottom right
                # self.vertices+=[x+1,y+1] # Top right
                # Top line is inserted every time.
                g.add_edge((x+1,y+1),(x,y+1))
                # self.vertices+=[x+1,y+1] # Top right
                # self.vertices+=[x,y+1] # top left
                # Left line is inserted if x==0
                if(x==0):
                    g.add_edge((x,y+1),(x,y))
                    # self.vertices+=[x,y+1] # top left
                    # self.vertices+=[x,y] # Bottom left
        (self.vertices,self.colors,self.indices) = graph_to_ogl(g)
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)
        self.colors = np.array(self.colors, dtype=np.float32)
        self.data_initialized=True

    # Updates the number of divisions and flags for gpu update. 
    def set_divisions(self, divisions):
        self.divisions=divisions
        self.generate_vertices()
        self.update=True
