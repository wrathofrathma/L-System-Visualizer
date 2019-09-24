from OpenGL import GL
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

        self.color = np.array([0.0, 0.0, 0.0, 1.0])
        self.wireframe=True
        #self.meshes = LContainer()
        self.quad = Quad()
    # Virtual functions inherited by QOpenGLWidget

    # Called whenever we want to update the widget
    def paintGL(self):
        GL.glClearColor(self.color[0], self.color[1], self.color[2], self.color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        #print("Number of meshes: " + str(len(self.meshes.meshes)))
        #self.meshes.draw()
        #self.mesh.draw()
        self.quad.draw()
        self.printOpenGLErrors()

    # Catch opengl errors between every draw.
    def printOpenGLErrors(self):
        pass

    # Sets up viewport, projection, other resize shenanigans
    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0,0,w,h)

    # CAlled once before resizeGL and paintGL.
    def initializeGL(self):
        print("[ INFO ] Initializing OpenGL...")
        self.loadShaders()
        GL.glClearColor(self.color[0], self.color[1], self.color[2], self.color[3])
        GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glDepthFunc(GL.GL_LESS)
        # Testing mesh stuff.
        self.quad.setShader(self.shader)
        #self.mesh = Mesh()
        #self.mesh.setShader(self.shader)
        #vertices = np.array([0.0,0.0,0.001,0.0,0.0,0.001], dtype=np.float32)
        #self.mesh.setVertices(vertices)
        #ogl.meshes.add_vertex(np.array([0.0,0.0], dtype=np.float32))
        #ogl.meshes.add_vertex(np.array([0.0,0.2], dtype=np.float32))
        #ogl.meshes.add_vertex(np.array([0.2,0.0], dtype=np.float32))

        #ogl.meshes.add_vertex(np.array([0.0,-1.0]))
        #ogl.meshes.add_vertex(np.array([0.0,0.0]))
        #ogl.meshes.add_vertex(np.array([0.5,0.5]))
        #ogl.meshes.add_vertex(np.array([0.5,0.0]))

    def toggleWireframe(self):
        print("[ INFO ] Toggling wireframe.")
        if(self.wireframe):
            GL.glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self.wireframe = False
        else:
            self.wireframe = True
            GL.glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Cleanup code for OpenGL. We need to cleanup our mesh objects and shaders from GPU memory or it'll leak.
    def cleanup(self):
        print("[ INFO ] Cleaning up display widget memory.")
        #self.meshes.cleanup()

    def loadShaders(self):
        print("[ INFO ] Loading shaders...")
        self.shader = Shader("assets/shaders/Default.vs", "assets/shaders/Default.fs")
        #self.meshes.setShader(self.shader)
        print("[ INFO ] Shaders loaded.")

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
