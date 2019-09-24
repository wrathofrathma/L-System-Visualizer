from OpenGL.GL import GLuint, glDeleteBuffers, glGenBuffers
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray, glDeleteVertexArrays

from OpenGL.arrays import ArrayDatatype
import numpy as np

class Drawable():
    def __init__(self):
        # We can't initialize our VAO here because we don't have a valid context if we create meshes outside of the 3 primary QT widget functions.
        self.VAO = GLuint(0)
        #glGenVertexArrays(1,self.VAO) # VertexArrayObject
        #self.VBO = glGenBuffers(1)
        self.VBO = GLuint(0)
        self.EBO = GLuint(0)
         # Vertex buffer ID
        self.vPos=0  # Shader vertex data position
        self.vColor=1 # Shader vertex color position
        self.vNorm=2 # Shader vertex normal position. For 3D Lighting later.

        self.uModel = GLuint(0) # Shader position of the model matrix. For later when we do 3D meshes and rotations.
        self.vertices = np.array([]) # Placeholder for vertices of our mesh
        self.shader = None # Shader object
        self.update = True # Update flag for updating our GPU data. Called in our draw function.
        self.initialized = False
    def draw(self):
        print("[ ERROR ] Define the draw function.")

    # Uploads the vertices and color data to the GPU. Virtual so that it's easy to differentiate between 2D/3D later.
    def updateGPU(self):
        print("[ ERROR ] Define the update function.")

    def init_ogl(self):
        print("[ INFO ] Initializing Drawable OpenGL buffers.")
        glGenVertexArrays(1,self.VAO)
        glGenBuffers(1, self.VBO)
        glGenBuffers(1, self.EBO)
        self.initialized=True
    # Deletes the data from the GPU. Should be the same for 2D & 3D
    def cleanup(self):
        GL.glDeleteVertexArrays(1, self.VAO)
        GL.glDeleteBuffers(1, self.VBO)

    def setShader(self, shader):
        self.shader = shader

    def setVertices(self, vertices):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.update=True

    def getVertices(self):
        return self.vertices
