# OpenGL testing using only built in shader class.
from OpenGL.GL import shaders
from OpenGL.GL import *
import ctypes
from PyQt5.QtWidgets import *
# from OpenGL.GL import GLuint, glDeleteBuffers, glGenBuffers, GL_ARRAY_BUFFER
# from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray, glDeleteVertexArrays

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np


class LSystemDisplayWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(LSystemDisplayWidget, self).__init__(parent)

    def paintGL(self):
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Binding VBO object
        glUseProgram(self.shader)
        glBindVertexArray(self.VAO)
        # Drawing
        glDrawArrays(GL_TRIANGLES, 0, 3)
        #Unbinding everything
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
        with open("assets/shaders/Default.vs","r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/Default.fs","r") as f:
            fc = "".join(f.readlines()[0:])
        print("[ INFO ] Loaded shader code...")
        print(vc)
        print(fc)
        vertex = shaders.compileShader(vc, GL_VERTEX_SHADER)
        fragment = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vertex,fragment)

        glUseProgram(self.shader)
        # Setting up the triangle & uploading to GPU
        self.VAO = GLuint(0)
        glGenVertexArrays(1, self.VAO)
        self.VBO = GLuint(0)
        glGenBuffers(1, self.VBO)
        self.vertices = np.array([0.0,0.0,0.5,0.5,0.0,0.5], dtype=np.float32)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.cast(0, ctypes.c_void_p))
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)
        glUseProgram(0)


    def cleanup(self):
        print("[ INFO ] Cleaning up display widget memory.")
        glDeleteVertexArrays(1,self.VAO)
        glDeleteBuffers(1, self.VBO)

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
