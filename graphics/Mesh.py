from OpenGL.GL import *

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np

class Mesh():
    def __init__(self):
        self.initialized=False
        self.update=True
        self.vertices = []

    def init_ogl(self):
        if(self.shader==None):
            print("[ ERROR ] Shader not set for our mesh.")
            exit(1)
        if(len(self.vertices)==0):
            print("[ ERROR ] Attempting to initialize an object with no vertices.")
            exit(1)

        # Setting up the triangle & uploading to GPU
        glUseProgram(self.shader)
        self.VBO = vbo.VBO(self.vertices, target=GL_ARRAY_BUFFER)
        self.initialized=True
        self.update=False # if we just initialized, we don't need to upload to gpu

    def set_shader(self, shader):
        self.shader = shader

    def set_vertices(self, vertices):
        self.vertices = vertices
        self.update = True

    def draw(self):
        if(self.initialized==False):
            self.init_ogl()
        if(self.update):
            self.update_gpu()
        # Binding VBO object
        self.VBO.bind()
        # Explaining to the GPU how to use the data.
        # Telling it that the VBO contains an array of vertices
        glEnableClientState(GL_VERTEX_ARRAY)
        # Telling the GPU the structure and type of data
        glVertexPointer(2, GL_FLOAT, 0, self.VBO)
        # Drawing
        print("Hello I'm drawing: " + str(self.vertices))

        glDrawArrays(GL_LINE_STRIP, 0, int(len(self.vertices) / 2.0))
        #Unbinding everything
        self.VBO.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        shaders.glUseProgram(0)

    def cleanup(self):
        self.VBO.delete()

    def update_gpu(self):
        self.update=False

        if(self.shader==None):
            print("[ ERROR ] Shader not set for our mesh.")
            exit(1)

        glUseProgram(self.shader)
        self.VBO.bind()
        self.VBO.set_array(self.vertices)
        self.VBO.copy_data()
        self.VBO.unbind()
        glUseProgram(0)

    def get_vertices(self):
        return self.vertices
