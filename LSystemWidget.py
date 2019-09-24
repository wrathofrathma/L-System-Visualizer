# OpenGL testing using built in VBO & shader convenience classes
from OpenGL.GL import shaders
from OpenGL.GL import *

from PyQt5.QtWidgets import *
# from OpenGL.GL import GLuint, glDeleteBuffers, glGenBuffers, GL_ARRAY_BUFFER
# from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray, glDeleteVertexArrays

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np

from graphics.Mesh import *

class LSystemDisplayWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(LSystemDisplayWidget, self).__init__(parent)
        self.bgcolor = np.array([1.0, 0.8, 0.9, .5])
        self.mesh = Mesh()
        vertices = np.array([0.0,0.0,0.5,0.5,0.0,0.5], dtype=np.float32)

        self.mesh.set_vertices(vertices)
    def paintGL(self):
        glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3])
        glClear(GL_COLOR_BUFFER_BIT)

        self.mesh.draw()

    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0,0,w,h)

    def initializeGL(self):
        print("[ INFO ] Initializing OpenGL...")
        self.loadShaders()
        self.mesh.set_shader(self.shader)

    def loadShaders(self):
        print("[ INFO ] Loading shaders...")
        with open("assets/shaders/Default.vs","r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/Default.fs","r") as f:
            fc = "".join(f.readlines()[0:])
        print("[ INFO ] Loaded shader code...")
        print(vc)
        print(fc)
        self.vs = shaders.compileShader(vc, GL_VERTEX_SHADER)
        self.fs = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(self.vs,self.fs)

        print("[ INFO ] Shaders loaded to graphics card.")

    def cleanup(self):
        print("[ INFO ] Cleaning up display widget memory.")

        # Cleaning up mesh memory on GPU
        self.mesh.cleanup()

        # Detaching shaders and deleting shader program
        glDetachShader(self.shader, self.vs)
        shaders.glDeleteShader(self.vs)
        glDetachShader(self.shader, self.fs)
        shaders.glDeleteShader(self.fs)
        glDeleteProgram(self.shader)

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
