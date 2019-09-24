from OpenGL.GL import *
from OpenGL.GL import shaders
from graphics.Drawable import *
from LContainer import *
from graphics.Shader import *

import numpy as np
from PyQt5.QtWidgets import *

from graphics.Mesh import *
from graphics.Quad import *
### TODO
# Shader loading
# Mesh drawing
# Camera class for moving around the scene
# Quaternion class for rotations
# Manually handle the framerate
# Light class


class LSystemDisplayWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(LSystemDisplayWidget, self).__init__(parent)

        self.bgcolor = np.array([1.0, 0.8, 0.9, .5])
        #self.meshes = LContainer()
        self.quad = Quad()

    # Called whenever we want to update the widget
    def paintGL(self):
        glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #self.meshes.draw()
        self.quad.draw()

    # Sets up viewport, projection, other resize shenanigans
    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0,0,w,h)

    # CAlled once before resizeGL and paintGL.
    def initializeGL(self):
        print("[ INFO ] Initializing OpenGL...")
        self.loadShaders()
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        self.quad.setShader(self.shader)

    # Cleanup code for OpenGL. We need to cleanup our mesh objects and shaders from GPU memory or it'll leak.
    def cleanup(self):
        print("[ INFO ] Cleaning up display widget memory.")
        #self.meshes.cleanup()

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

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    l1 = QLabel('Label 1')
    l2 = QLabel('Label 2')
    ogl = LSystemDisplayWidget()
    #layout.addWidget(l1)
    layout.addWidget(ogl)
    #layout.addWidget(l2)


    window.setLayout(layout)
    window.show()

    app.exec_()
