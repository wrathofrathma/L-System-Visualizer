from OpenGL import GL
from OpenGL.GL import shaders
from graphics.Drawable import *
from graphics.Mesh import *
from graphics.Shader import *

import numpy as np
from PyQt5.QtWidgets import *


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

        self.color = np.array([0.0, 0.3, 0.0, 1.0])
        self.wireframe=True
        self.mesh = Mesh()
    # Virtual functions inherited by QOpenGLWidget

    # Called whenever we want to update the widget
    def paintGL(self):
        GL.glClearColor(self.color[0], self.color[1], self.color[2], self.color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.mesh.draw()
        self.printOpenGLErrors()

    # Catch opengl errors between every draw.
    def printOpenGLErrors(self):
        pass

    # Sets up viewport, projection, other resize shenanigans
    def resizeGL(self, w, h):
        pass

    # CAlled once before resizeGL and paintGL.
    def initializeGL(self):

        GL.glClearColor(self.color[0], self.color[1], self.color[2], self.color[3])
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)

    def toggleWireframe(self):
        if(self.wireframe):
            GL.glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self.wireframe = False
        else:
            self.wireframe = True
            GL.glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Cleanup code for OpenGL. We need to cleanup our mesh objects and shaders from GPU memory or it'll leak.
    def cleanup(self):
        self.mesh.cleanup()

    def loadShaders(self):
        self.shader = Shader("assets/shaders/Default.vs", "assets/shaders/Default.fs")

        print("Yeah bitch")
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
ogl.loadShaders()

app.exec_()
