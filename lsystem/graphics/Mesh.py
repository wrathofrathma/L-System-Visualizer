from OpenGL.GL import *

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np
from lsystem.graphics.QuaternionObject import *
from glm import value_ptr
import random as rand


from enum import Enum
# Enumeration for mesh options.
# Will be performing a bitwise operation on each option, higher numbers will win out in priority.
# I know it's redundant to have white vs colors, and pulse vs static, but think of them as aliases for their complements.
class MeshOptions():
    White=1
    Colors=2
    Pulse=4
    Static=8

class Mesh(QuaternionObject):
    def __init__(self, dimensions=2):
        super().__init__()
        self.initialized=False
        self.update=True
        self.vertices = []
        self.colors = []
        self.dimensions=dimensions
        self.translate([-0.5, 0, 0])
        self.options = MeshOptions.White | MeshOptions.Static

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
        self.update=True
        glUseProgram(0)

    # uses built in numpy array functions to detect the max/min X&Y values so we can center the mesh on display.
    # Returns 2 tuples, for maxes and mins.
    def detect2DEdges(self):
        v = np.array(self.vertices)
        v = v.reshape(int(v.shape[0]/2), 2)
        xs = v[:,0] # numpy 2d array slicing to get the xs
        ys = v[:,1] # Same but for ys.
        return (xs.max(), ys.max()), (xs.min(),ys.min())

    def generate_colors(self):
        # Each vertex needs a color.
        self.colors = []
        for v in range(len(self.vertices)):
            if(self.options & MeshOptions.Colors):
                self.colors.append(rand.randint(0,255)/255.0)
                self.colors.append(rand.randint(0,255)/255.0)
                self.colors.append(rand.randint(0,255)/255.0)
            else:
                self.colors.append(1)
                self.colors.append(1)
                self.colors.append(1)

            self.colors.append(0)
        self.colors = np.array(self.colors, dtype=np.float32)

    def set_options(self, options):
        self.options = options

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
        shaders.glUseProgram(self.shader)
        # Generate model matrix
        self.generateModelMatrix()
        # Update uniforms on shader.
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "model"), 1, GL_FALSE, value_ptr(self.model_matrix))

        # Binding VBO object
        self.VBO.bind()
        # Explaining to the GPU how to use the data.
        #Enable shader positional variables
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        # Tell GLSL how our data is structured
        # Vertices are in position 0, size of 2 floats, padding of 0, at self.VBO
        glVertexAttribPointer(0, self.dimensions, GL_FLOAT, False, 0, self.VBO)
        # Colors are in position 1, size of 4 floats, padding of 0, and at the end of the vertice array.
        glVertexAttribPointer(1, 4, GL_FLOAT, True, 0, self.VBO+self.vertices.nbytes)

         # Drawing
        glDrawArrays(GL_LINE_STRIP, 0, int(len(self.vertices) /self.dimensions))

        #Unbinding everything
        self.VBO.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        shaders.glUseProgram(0)

    def cleanup(self):
        self.VBO.delete()

    def update_gpu(self):
        self.update=False

        if(self.shader==None):
            print("[ ERROR ] Shader not set for our mesh.")
            exit(1)
        # Generate colors if they don't exist.
        if(len(self.colors)==0):
            self.generate_colors()

        data = [] # Verts + colors
        data+=self.vertices.tolist()
        data+=self.colors.tolist()
        data=np.array(data, dtype=np.float32)

        glUseProgram(self.shader)
        self.VBO.bind()
        self.VBO.set_array(data)
        self.VBO.copy_data()
        self.VBO.unbind()
        glUseProgram(0)

    def get_vertices(self):
        return self.vertices
