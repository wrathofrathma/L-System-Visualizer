from OpenGL.GL import shaders
from OpenGL.GL import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from OpenGL.arrays import ArrayDatatype, vbo
import numpy as np

from lsystem.graphics.Mesh import *
from time import time
from lsystem.lsystem_utils import *
from PIL import Image
from lsystem.graphics.SphericalCamera import *
from lsystem.graphics.FreeCamera import *

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
        self.keep_centered = True # Boolean for whether to center the mesh after resizes.
        self.camera = FreeCamera(800,600)
        #self.camera = SphericalCamera(800,600)
        #self.camera.r = -4
        # self.camera.updateView()
    # This is from QOpenGLWidget, this is where all drawing is done.
    def paintGL(self):
        glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.camera.update()
        self.camera.applyUpdate(self.shader)
        for mesh in self.meshes:
            mesh.draw()


    # Triggered when the mouse is pressed in the opengl frame.
    def mousePressEvent(self, event):
        if(event.button()==Qt.LeftButton):
            self.zoomOnMouse((event.pos()))

        elif(event.button()==Qt.RightButton):
            # Zoom in
            self.camera.translate([0,0,0.2])
            self.update()
        elif(event.button()==Qt.MidButton):
            self.resetCamera()
    # Converts a qt mouse position event coordinates to opengl coordinates
    # aka top left from(0,0) to bottom left being (-1,-1) and top right being (1,1)
    def qtPosToOGL(self, pos):
        # Subtract 1/2 the screen w/h from the pos.
        qpos = np.array([pos.x(), pos.y()])
        wsize = np.array([self.size().width(), self.size().height()])
        print("Qpos : " + str(qpos))
        print("Wsize: " + str(wsize))
        return qpos - wsize

    def zoomOnMouse(self, pos):
        print("zooming on mouse pos: " + str(pos))
        print("OpengL window size: " + str((self.size())))
        print("Mouse Pos to OGL: " + str(self.qtPosToOGL(pos)))
        self.camera.translate([0,0,-0.2])
        self.update()

    # Resets camera to default position & orientation
    def resetCamera(self):
        self.camera.setPosition([0,0,1])
        self.camera.setOrientation(0)
        self.update()

    # Triggered only when the mouse is dragged in the opengl frame with the mouse down(on my machine)
    def mouseMoveEvent(self, event):
        pass
    # Called when the OpenGL widget resizes.
    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0,0,w,h)
        self.camera.resize(w,h)

        if(self.keep_centered):
            self.center_mesh()

    # Defines whether to keep the mesh centered in the view after resizes.
    def center_on_resize(self, val):
        self.keep_centered = val

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

    # Centers the mesh in the view
    def center_mesh(self):
        # Well, since we have multiple meshes, we need the mins and maxes of all of them before slicing.
        maxes=[]
        mins= []
        for mesh in self.meshes:
            ma, mi = mesh.detect2DEdges()
            maxes.append(ma)
            mins.append(mi)
        # this should create 2, (n,2) dimension numpy arrays.
        maxes = np.array(maxes)
        mins = np.array(mins)
        max_x = maxes[:,0].max()
        max_y = maxes[:,1].max()
        min_x = mins[:,0].min()
        min_y = mins[:,1].min()

        print("Min_x: %3.2f, Max_x: %3.2f, Min_y: %3.2f, Max_y: %3.2f" % (min_x, max_x,min_y, max_y))
    # Sets the vertices of the last mesh in the array.
    # split=True creates a new mesh before setting the vertices.
    def set_vertices(self, vertices, split=False):
        if(split):
            self.meshes.append(Mesh())
            self.meshes[-1].set_shader(self.shader)

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
