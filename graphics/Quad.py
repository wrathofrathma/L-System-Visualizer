from OpenGL.GL import *
import numpy as np
from graphics.Drawable import *

class Quad(Drawable):
    def __init__(self):
        super().__init__()
        self.vertices = np.array([-0.5, -0.5, 0.5, -0.5, 0.0, 0.5])

    def draw(self):
        if(len(self.vertices)==0):
            print("[ ERROR ] Empty vertices")
            return 0
        if(self.update):
            self.updateGPU()
        if(self.shader!=None):
            # Bind shader & VAO
            glUseProgram(self.shader)
            self.VBO.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2,GL_FLOAT, 0, self.VBO)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            self.VBO.unbind()
            glDisableClientState(GL_VERTEX_ARRAY)
            shaders.glUseProgram(0)
    def updateGPU(self):
        print("[ INFO ] Updating GPU")
        if(self.shader==None):
            print("[ ERROR ] Shader not set, aborting update.")
            return
        if(len(self.vertices)==0):
            print("[ ERROR ] Vertice count = 0, aborting update.")
            return
        if(self.initialized==False):
            self.init_ogl()
        glUseProgram(self.shader)
        self.VBO.bind()
        self.VBO.set_array(self.vertices)
        self.VBO.unbind()
        glUseProgram(0)
        print("[ INFO ] Finished update")
