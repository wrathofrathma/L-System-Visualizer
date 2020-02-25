# This file will draw the 3D Axis
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    shaders,
    glUniformMatrix4fv,
    GL_FALSE,
    glGetUniformLocation,
    glEnableVertexAttribArray,
    glVertexAttribPointer,
    GL_FLOAT,
    glDrawArrays,
    GL_LINES,
    glUseProgram,
    GL_VERTEX_ARRAY,
    GL_COLOR_ARRAY,
    glDisableClientState,
)

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np
from lsystem.graphics.quaternion_object import QuaternionObject
from glm import value_ptr


class Axis(QuaternionObject):
    def __init__(self):
        super().__init__()
        self.initialized = False
        self.update = True
        self.vertices = np.array(
            [0, 0, -10, 0, 0, 10, -10, 0, 0, 10, 0, 0, 0, -10, 0, 0, 10, 0],
            dtype=np.float32,
        )
        self.colors = np.array(
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            dtype=np.float32,
        )

    def init_ogl(self):
        if self.shader == None:
            print("[ ERROR ] Shader not set for our mesh.")
            exit(1)

        # Setting up the triangle & uploading to GPU
        glUseProgram(self.shader)
        self.VBO = vbo.VBO(self.vertices, target=GL_ARRAY_BUFFER)
        self.initialized = True
        self.update = True
        glUseProgram(0)

    def set_shader(self, shader):
        self.shader = shader

    def draw(self):
        if self.initialized == False:
            self.init_ogl()
        if self.update:
            self.update_gpu()
        shaders.glUseProgram(self.shader)
        # Generate model matrix
        self.generate_model_matrix()
        # Update uniforms on shader.
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "model"),
            1,
            GL_FALSE,
            value_ptr(self.model_matrix),
        )

        # Binding VBO object
        self.VBO.bind()
        # Explaining to the GPU how to use the data.
        # Enable shader positional variables
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        # Tell GLSL how our data is structured
        # Vertices are in position 0, size of 3 floats, padding of 0, at self.VBO
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, self.VBO)
        # Colors are in position 1, size of 4 floats, padding of 0, and at the end of the vertice array.
        glVertexAttribPointer(1, 4, GL_FLOAT, True, 0, self.VBO + self.vertices.nbytes)

        # Drawing
        glDrawArrays(GL_LINES, 0, int(len(self.vertices) / 3))

        # Unbinding everything
        self.VBO.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        shaders.glUseProgram(0)

    def cleanup(self):
        self.VBO.delete()

    def update_gpu(self):
        self.update = False

        if self.shader == None:
            print("[ ERROR ] Shader not set for our mesh.")
            exit(1)

        data = []  # Verts + colors
        data += self.vertices.tolist()
        data += self.colors.tolist()
        data = np.array(data, dtype=np.float32)

        glUseProgram(self.shader)
        self.VBO.bind()
        self.VBO.set_array(data)
        self.VBO.copy_data()
        self.VBO.unbind()
        glUseProgram(0)
