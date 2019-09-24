from OpenGL.GL import GLuint, glDeleteBuffers, glGenBuffers, GL_ARRAY_BUFFER
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray, glDeleteVertexArrays

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np

class Drawable():
    def __init__(self):

        self.vPos=0  # Shader vertex data position
        self.VBO = GLuint(0)
        self.vertices = np.array([]) # Placeholder for vertices of our mesh
        self.shader = None # Shader object
        self.update = True # Update flag for updating our GPU data. Called in our draw function.
        self.initialized = False

    def draw(self):
        print("[ ERROR ] Define the draw function.")

    # Uploads the vertices and color data to the GPU. Virtual so that it's easy to differentiate between 2D/3D later.
    def updateGPU(self):
        print("[ ERROR ] Define the update function.")

    # Should only ever be called when we know self.vertices exists so our vbo has a valid data
    def init_ogl(self):
        print("[ INFO ] Initializing OpenGL VBO.")
        self.VBO = vbo.VBO(np.zeros(1), target = GL_ARRAY_BUFFER)
        self.initialized=True

    # Deletes the data from the GPU. Should be the same for 2D & 3D
    def cleanup(self):
        self.VBO.delete()

    def setShader(self, shader):
        self.shader = shader

    def setVertices(self, vertices):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.update=True

    def getVertices(self):
        return self.vertices
