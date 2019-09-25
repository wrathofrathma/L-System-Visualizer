# OpenGL testing using built in VBO & shader convenience classes
from OpenGL.GL import shaders
from OpenGL.GL import *

from PyQt5.QtWidgets import *
# from OpenGL.GL import GLuint, glDeleteBuffers, glGenBuffers, GL_ARRAY_BUFFER
# from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray, glDeleteVertexArrays

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np


class LSystemDisplayWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(LSystemDisplayWidget, self).__init__(parent)
        self.bgcolor = np.array([1.0, 0.8, 0.9, .5])

    def paintGL(self):
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        shaders.glUseProgram(self.shader)
        # Binding VBO object
        self.VBO.bind()
        # Explaining to the GPU how to use the data.
        # Telling it that the VBO contains an array of vertices
        glEnableClientState(GL_VERTEX_ARRAY)
        # Telling the GPU the structure and type of data
        glVertexPointer(2, GL_FLOAT, 0, self.VBO)
        # Drawing
        glDrawArrays(GL_TRIANGLES, 0, 3)
        #Unbinding everything
        self.VBO.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        shaders.glUseProgram(0)

    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0,0,w,h)

    def initializeGL(self):
        print("[ INFO ] Initializing OpenGL...")
        #glEnable(GL_DEPTH_TEST)
        #glDepthFunc(GL_LESS)

        # Shader loading
        # with open("assets/shaders/Default.vs","r") as f:
        #     vc = "".join(f.readlines()[0:])
        # with open("assets/shaders/Default.fs","r") as f:
        #     fc = "".join(f.readlines()[0:])
        # print("[ INFO ] Loaded shader code...")
        # print(vc)
        # print(fc)
        # vertex = shaders.compileShader(vc, GL_VERTEX_SHADER)
        # fragment = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
        # self.shader = shaders.compileProgram(vertex,fragment)
        self.loadShaders()

        glUseProgram(self.shader)
        # Setting up the triangle & uploading to GPU
        self.vertices = np.array([0.0,0.0,0.5,0.5,0.0,0.5], dtype=np.float32)
        self.VBO = vbo.VBO(self.vertices, target=GL_ARRAY_BUFFER)

    def loadShaders(self):
        print("[ INFO ] Loading shaders...")
        with open("assets/shaders/Default.vs","r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/Default.fs","r") as f:
            fc = "".join(f.readlines()[0:])
        print("[ INFO ] Loaded shader code...")

        vertex = shaders.compileShader(vc, GL_VERTEX_SHADER)
        fragment = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vertex,fragment)
        print("[ INFO ] Shaders loaded to graphics card.")

    def cleanup(self):
        print("[ INFO ] Cleaning up display widget memory.")
        self.VBO.delete()

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    l1 = QLabel('Label 1')
    l2 = QLabel('Label 2')
    ogl = LSystemDisplayWidget()
    layout.addWidget(ogl)


    window.setLayout(layout)
    window.show()

    app.exec_()
    ogl.cleanup()
