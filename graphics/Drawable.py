from OpenGL import GL
import numpy as np

class Drawable():
    def __init__(self):
        self.VAO = GL.GLuint(0) # VertexArrayObject
        self.VBO = GL.GLuint(0) # VertexBufferObject

        self.vPos=0  # Shader vertex data position
        self.vNorm=1 # Shader vertex normal position
        self.vColor=2 # Shader vertex color position
        self.uModel = GL.GLuint(0) # Shader position of the model matrix
        self.vertices = np.array() # Vertices of our mesh
        self.shader = None # Shader object
        self.update = True # Update flag for updating our GPU data. Called in our draw function.

    def draw(self):
        pass

    def updateGPU(self):
        self.update=False


    def cleanup(self):
        GL.glDeleteVertexArrays(1, self.VAO)
        GL.glDeleteBuffers(1, self.VBO)

    def setShader(self, shader):
        self.shader = shader

    def setVertices(self, vertices):
        self.vertices = vertices
        self.update=True
