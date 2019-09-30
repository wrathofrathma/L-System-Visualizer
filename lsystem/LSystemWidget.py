# OpenGL testing using built in VBO & shader convenience classes
from OpenGL.GL import shaders
from OpenGL.GL import *

from PyQt5.QtWidgets import *

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np

from graphics.Mesh import *
from time import time
from lsystem.lsystem_utils import *
from PIL import Image

class LSystemDisplayWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(LSystemDisplayWidget, self).__init__(parent)
        self.bgcolor = np.array([0.0, 0.0, 0.0, 0.0])
        self.start_time = time()
        self.mesh = Mesh()
        #self.meshes = []
        #self.meshes.append(Mesh())
        verts = get_saved_lsystem('Cantor Set')[0]
        self.mesh.set_vertices(verts)

    def paintGL(self):
        glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #for mesh in self.meshes:
        self.mesh.draw()

    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0,0,w,h)

    def initializeGL(self):
        print("[ INFO ] Initializing OpenGL...")
        self.loadShaders()
        print("[ INFO ] Shader ID: " + str(self.shader))
        #self.meshes[-1].set_shader(self.shader)
    #    glLineWidth(5)
        # glEnable(GL_DEPTH_TEST)
        # glDepthFunc(GL_LEQUAL)
        self.mesh.set_shader(self.shader)


    def loadShaders(self):
        print("[ INFO ] Loading shaders...")
        with open("assets/shaders/Default.vs","r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/Default.fs","r") as f:
            fc = "".join(f.readlines()[0:])
        print("[ INFO ] Loaded shader code...")

        try:
            self.vs = shaders.compileShader(vc, GL_VERTEX_SHADER)
            self.fs = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
            self.shader = shaders.compileProgram(self.vs, self.fs)
        except Exception as err:
            print("[ ERROR ] Caught an exception: " + str(err))
        print("[ INFO ] Shaders loaded to graphics card.")

    # Saves a screenshot of the current OpenGL buffer to a given filename.
    # MUST have a file extension for now. 
    def screenshot(self, filename):
        print("[ INFO ] Saving screenshot to filename " + str(filename) + "...")
        size = self.size()
        pixels = glReadPixels(0,0, size.width(), size.height(), GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (size.width(), size.height()), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(filename)
        print("[ INFO ] Saved.")

    def cleanup(self):
        print("[ INFO ] Cleaning up display widget memory.")

        # Cleaning up mesh memory on GPU
        self.mesh.cleanup()
        #self.meshes.cleanup()

        # Detaching shaders and deleting shader program
        glDetachShader(self.shader, self.vs)
        shaders.glDeleteShader(self.vs)
        glDetachShader(self.shader, self.fs)
        shaders.glDeleteShader(self.fs)
        glDeleteProgram(self.shader)

    # Adds vertices to whatever the active mesh is.
    def add_vertices(self, vertices, mesh_num=0):
        self.mesh.set_vertices(vertices)
    #     if(len(self.meshes)<(mesh_num-1)):
    #         print("[ ERROR ] Can't add vertices to mesh. Invalid indice number.")
    #
    #     vs = self.meshes[mesh_num].get_vertices()
    #     vs = np.append(vs, vertices)
    #     self.meshes[mesh_num].set_vertices(vs)
    #

    def set_bg_color(self, color):
        if(len(color)==4):
            self.bgcolor = np.array(color, dtype=np.float32)
        elif(len(color==3)):
            self.bgcolor = np.array(color[0], color[1], color[2], 0.0, dtype=np.float32)
        else:
            print("")
        self.bgcolor = color


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
