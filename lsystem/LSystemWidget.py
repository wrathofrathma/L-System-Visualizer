from OpenGL.GL import shaders
from OpenGL.GL import *

from PyQt5.QtWidgets import *

from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np

from lsystem.graphics.Mesh import *
from time import time
from lsystem.lsystem_utils import *
from PIL import Image
from lsystem.graphics.SphericalCamera import *

# LSystem visualization widget.

class LSystemDisplayWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(LSystemDisplayWidget, self).__init__(parent)
        # Background color
        self.bgcolor = np.array([0.0, 0.0, 0.0, 0.0])
        # Time, used for color shader shenanigans
        self.start_time = time()
        # Mesh initialization & starting stuff.
        self.meshes = []
        self.meshes.append(Mesh())
        verts = get_saved_lsystem('Cantor Set')[0]
        self.meshes[0].set_vertices(verts[0])

        self.camera = SphericalCamera(800,600)
        #self.camera.r = -4
    # This is from QOpenGLWidget, this is where all drawing is done.
    def paintGL(self):
        glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        self.camera.applyUpdate(self.shader)
        for mesh in self.meshes:
            mesh.draw()

    # Called when the OpenGL widget resizes.
    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0,0,w,h)
        self.camera.resize(w,h)

    # OpenGL initialization
    def initializeGL(self):
        print("[ INFO ] Initializing OpenGL...")
        self.loadShaders()
        print("[ INFO ] Shader ID: " + str(self.shader))
    #    glLineWidth(5)
        # Set the shader for every mesh
        for mesh in self.meshes:
            mesh.set_shader(self.shader)


    def loadShaders(self):
        # Load the shader files into a string.
        print("[ INFO ] Loading shaders...")
        with open("assets/shaders/Default.vs","r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/Default.fs","r") as f:
            fc = "".join(f.readlines()[0:])
        print("[ INFO ] Loaded shader code...")
        try:
            # Compile hte shaders on the graphics card.
            self.vs = shaders.compileShader(vc, GL_VERTEX_SHADER)
            self.fs = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
            # Link them together & compile them as a program.
            self.shader = shaders.compileProgram(self.vs, self.fs)
        except Exception as err:
            print("[ ERROR ] Caught an exception: " + str(err))
            exit(1) # Can't proceed without working shaders.

        print("[ INFO ] Shaders loaded to graphics card.")

    # Saves a screenshot of the current OpenGL buffer to a given filename.
    # MUST have a file extension for now.
    def screenshot(self, filename):
        print("[ INFO ] Saving screenshot to filename " + str(filename) + "...")
        size = self.size()
        # Read all of the pixels into an array.
        pixels = glReadPixels(0,0, size.width(), size.height(), GL_RGB, GL_UNSIGNED_BYTE)
        # Create an image from Python Image Library.
        image = Image.frombytes("RGB", (size.width(), size.height()), pixels)
        # FLip that bitch.
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(filename)
        print("[ INFO ] Saved.")

    # Cleanups all shader memory & mesh data.
    def cleanup(self):
        print("[ INFO ] Cleaning up display widget memory.")

        # Cleaning up mesh memory on GPU
        self.clear_mesh()

        # Detaching shaders and deleting shader program
        #glDetachShader(self.shader, self.vs)
        #glDetachShader(self.shader, self.fs)
        glDeleteShader(self.vs)

        glDeleteShader(self.fs)
        glDeleteProgram(self.shader)

    # Sets the vertices of the last mesh in the array.
    # split=True creates a new mesh before setting the vertices.
    def set_vertices(self, vertices, split=False):
        if(split):
            self.meshes.append(Mesh())
        self.meshes[-1].set_vertices(vertices)

    # Cleans up the mesh memory on the GPU and clears the array of them.
    def clear_mesh(self):
        for mesh in self.meshes:
            mesh.cleanup()
        self.meshes.clear()
        self.meshes.append(Mesh())
        self.meshes[-1].set_shader(self.shader)

    # Sets the background color of the OpenGL widget.
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
