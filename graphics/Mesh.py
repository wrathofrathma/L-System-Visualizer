from OpenGL import GL
from OpenGL.GL import *
import numpy as np
from graphics.Drawable import *

# OpenGL Mesh class.
# Drawing line by line with thousands of objects would take significantly longer periods of time than just deleting/reallocating memory and uploading a new
# mesh.

class Mesh(Drawable):
    def __init__(self):
        super().__init__()

    # TODO Fix the framerate on this. Seems to only update when PyQT wants us to.
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
            # Draw
            print(len(self.vertices) / 2)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            # Unbind shader & VAO
            glUseProgram(0)
            glBindVertexArray(0)

        print("Drawing Update")


    def updateGPU(self):
        print("[ INFO ] Updating GPU")
        if(self.shader==None):
            print("[ ERROR ] Shader not set, aborting update.")
            return
        if(len(self.vertices)==0):
            print("[ ERROR ] Vertice count = 0, aborting update.")
            return

        # Get sizes of things
        vertice_size = ArrayDatatype.arrayByteCount(self.vertices)

        self.shader.bind()
        self.update=False

        glBindVertexArray(self.VAO)
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
        print("[ INFO ] Finished update")
