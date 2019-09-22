from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype
import numpy as np

class Drawable():
    def __init__(self):
        self.VAO = GLuint(0) # VertexArrayObject
        self.VBO = glGenBuffers(1)
         # Vertex buffer ID
        self.vPos=0  # Shader vertex data position
        self.vNorm=1 # Shader vertex normal position
        self.vColor=2 # Shader vertex color position
        self.uModel = GLuint(0) # Shader position of the model matrix
        self.vertices = np.array([]) # Placeholder for vertices of our mesh
        self.shader = None # Shader object
        self.update = True # Update flag for updating our GPU data. Called in our draw function.

    def draw(self):
        pass

    def updateGPU(self):
        print("Updating GPU")
        self.update=False
        glBindVertexArray(self.VAO)
        # Allocate space for data
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        # Upload data
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(self.vertices), self.vertices, GL_DYNAMIC_DRAW)

        # Tell opengl how to work this data
        glVertexAttribPoiner(self.vPos, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(self.vPos)

        # Unbind buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        print("Finished update")
    def cleanup(self):
        GL.glDeleteVertexArrays(1, self.VAO)
        GL.glDeleteBuffers(1, self.VBO)

    def setShader(self, shader):
        self.shader = shader

    def setVertices(self, vertices):
        self.vertices = vertices
        self.update=True

    def getVertices(self):
        return self.vertices
