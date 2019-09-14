from OpenGL import GL
from OpenGL.GL import shaders
import numpy as np

class Drawable():
    def __init__(self):
        self.VAO = GL.GLuint(0) # VertexArrayObject
        self.VBO = GL.GLuint(0) # VertexBufferObject

        self.vPos=0  # Shader vertex data position
        self.vNorm=1 # Shader vertex normal position
        self.vColor=2 # Shader vertex color position
        self.uModel = GL.GLuint(0) # Shader position of the model matrix
        self.vertices = np.array()

    def draw(self):
        pass

    def updateGPU(self):
        pass
