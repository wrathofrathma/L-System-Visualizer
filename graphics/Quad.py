from OpenGL.GL import *
import numpy as np
from graphics.Drawable import *

class Quad(Drawable):
    def __init__(self):
        super().__init__()
        #self.EBO = glGenBuffers(1)
        self.dims = [1,1,1,1]
        self.generateQuad()

    def draw(self):
        if(len(self.vertices)==0):
            print("[ ERROR ] Empty vertices")
            return 0
        if(self.update):
            self.updateGPU()
        if(self.shader!=None):
            # Bind shader & VAO
            self.shader.bind()
            glBindVertexArray(self.VAO)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
            # Draw
            print("Drawing")
            glDrawElements(GL_POINTS, len(self.indices), GL_UNSIGNED_INT, 0)
            # Unbind shader & VAO
            glUseProgram(0)
            glBindVertexArray(0)

    def updateGPU(self):
        if(self.initialized==False):
            self.init_ogl()
        print("[ INFO ] Updating GPU")
        if(self.shader==None):
            print("[ ERROR ] Shader not set, aborting update.")
            return
        if(len(self.vertices)==0):
            print("[ ERROR ] Vertice count = 0, aborting update.")
            return

        # Get sizes of things
        vertice_size = ArrayDatatype.arrayByteCount(self.vertices)
        indice_size = ArrayDatatype.arrayByteCount(self.indices)
        print("Loading vertices & indices of size: " + str(vertice_size) + " " + str(indice_size))
        self.shader.bind()

        glBindVertexArray(self.VAO)
        # Load indices

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        print("test 1")
        # NoneType object is not callable???
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indice_size, self.indices, GL_DYNAMIC_DRAW)
        print("test 2")
        # Allocate space for data
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        # Upload data
        glBufferData(GL_ARRAY_BUFFER, vertice_size, self.vertices, GL_DYNAMIC_DRAW)

        # Tell opengl how to work this data
        glVertexAttribPointer(self.vPos, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(self.vPos)
        # Unbind buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        self.update=False
        print("[ INFO ] Finished update")

    def setDimensions(self, dims):
        self.dims

    def generateQuad(self):
        x = self.dims[0]
        y = self.dims[1]
        z = self.dims[2]
        w = self.dims[3]

        self.vertices = np.array([x/2.0, y/2.0, z/2.0, -y/2.0, -z/2.0, -w/2.0, -x/2.0, w/2.0], dtype=np.float32)
        self.indices = np.array([0,1,3,1,2,3], dtype=np.uint32)
