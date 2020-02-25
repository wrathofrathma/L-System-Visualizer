# Generic class for drawing anything exported from the Graph class.

from OpenGL.GL import *

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np
from graphics.QuaternionObject import *
from glm import value_ptr
from ctypes import c_void_p

from graphics.colors import Colors
from lsystem.graph import *


# This class is a gridspace that overlays the l-system and detects intersections in individual gridspaces.
# It has n divisions across the X & Y axis.
class GraphObject(QuaternionObject):
    def __init__(self, dimensions=2):
        super().__init__()
        # OpenGL specific code
        self.dimensions = dimensions
        self.data_initialized = (
            False  # Flag for whether we've actually set the graph data.
        )
        self.opengl_initialized = (
            False  # Flag for whether we've initalized the opengl objects
        )
        self.update = (
            True  # Flag for whether we need to update our data on teh graphics card.
        )
        self.vertices = []
        self.colors = []
        self.indices = []
        # self.translate([-0.5,-0.5,0])

    def init_ogl(self):
        if self.shader == None:
            print("[ ERROR ] Shader not set for our mesh.")
            return
        if len(self.vertices) == 0:
            print("[ ERROR ] Attempting to initialize an object with no vertices.")
            exit(1)
        if len(self.indices) == 0:
            print(
                "[ ERROR ] Attempting to initialize an indexed vertex object with no indices."
            )
            exit(1)
        # Setting up the triangle & uploading to GPU
        glUseProgram(self.shader)
        # Indice buffer
        self.EBO = vbo.VBO(self.indices, target=GL_ELEMENT_ARRAY_BUFFER)
        # Vertex buffer
        self.VBO = vbo.VBO(self.vertices, target=GL_ARRAY_BUFFER)
        self.initialized = True
        self.update = True
        glUseProgram(0)

    # Clears the vertices, colors, indices
    def clear_graph(self):
        self.vertices = []
        self.colors = []
        self.indices = []
        self.data_initialized = False

    # The function to pass exported graph data to.
    def set_graph_data(self, graph):
        self.vertices, self.colors, self.indices = graph_to_ogl(graph)
        self.data_initialized = True

    def detect_2d_edges(self):
        v = np.array(self.vertices)
        v = v.reshape(int(v.shape[0] / 2), 2)
        xs = v[:, 0]  # numpy 2d array slicing to get the xs
        ys = v[:, 1]  # Same but for ys.
        return (xs.max(), ys.max()), (xs.min(), ys.min())

    def set_shader(self, shader):
        self.shader = shader

    def draw(self):
        # We can't initialized opengl without data currently.
        if self.data_initialized == False:
            return
        # Can't upload data to gpu without initializing buffers
        if self.opengl_initialized == False:
            self.init_ogl()
        # Can't draw if no data is uploaded to the gpu
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

        # Binding vertex buffer object and index buffer.
        self.VBO.bind()
        self.EBO.bind()

        # Explaining to the GPU how to use the data.
        # Enable shader positional variables
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        # Tell GLSL how our data is structured
        # Vertices are in position 0, size of 2 or 3 floats, padding of 0, at self.VBO
        glVertexAttribPointer(0, self.dimensions, GL_FLOAT, False, 0, self.VBO)
        # Colors are in position 1, size of 4 floats, padding of 0, and at the end of the vertice array.
        glVertexAttribPointer(1, 4, GL_FLOAT, True, 0, self.VBO + self.vertices.nbytes)

        # Drawing
        glDrawElements(GL_LINES, len(self.indices), GL_UNSIGNED_INT, None)

        # Unbinding everything
        self.VBO.unbind()
        self.EBO.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        shaders.glUseProgram(0)

    def cleanup(self):
        if self.opengl_initialized:
            self.VBO.delete()
            self.EBO.delete()

    def update_gpu(self):
        self.update = False

        if self.shader == None:
            print("[ ERROR ] Shader not set for our mesh.")
            exit(1)

        # Format our data for the GPU
        data = []  # Verts + colors
        data += self.vertices.tolist()
        data += self.colors.tolist()
        data = np.array(data, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)
        # Copy data to the graphics card.
        glUseProgram(self.shader)
        self.VBO.bind()
        self.VBO.set_array(data)
        self.VBO.copy_data()
        self.VBO.unbind()

        self.EBO.bind()
        self.EBO.set_array(self.indices)
        self.EBO.copy_data()
        self.EBO.unbind()
        glUseProgram(0)
