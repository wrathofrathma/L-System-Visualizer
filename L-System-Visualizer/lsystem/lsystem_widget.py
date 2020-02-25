"""This file handles the OpenGL Window actions"""
# Python core includes
from PIL import Image
from time import time

# PyQt includes
from PyQt5.QtWidgets import (
    QOpenGLWidget,
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
)

from PyQt5.QtCore import QTimer

# OpenGL includes
from OpenGL.GL import (
    glClearColor,
    glClear,
    shaders,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    glUseProgram,
    glUniform1f,
    glGetUniformLocation,
    glViewport,
    glGetString,
    GL_VERSION,
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER,
    glReadPixels,
    GL_RGB,
    GL_UNSIGNED_BYTE,
    glDeleteShader,
    glDeleteProgram,
)

# Lsystem includes
from glm import vec3
from graphics.spherical_camera import SphericalCamera
from graphics.free_camera import FreeCamera

from graphics.colors import Colors
from graphics.graph_mesh import GraphObject
from lsystem.graph import Graph

# Other includes
import numpy as np


# Legit just an enumeration for determining camera type in a readable manner.
class CameraType:

    Free = 0
    Orbital = 1


class LSystemDisplayWidget(QOpenGLWidget):
    def __init__(self):
        super(LSystemDisplayWidget, self).__init__()
        # Background color
        self.bgcolor = Colors.black
        self.start_time = time()

        # Production scene objects.
        self.graph = Graph()
        self.meshes = []
        self.meshes.append(GraphObject())
        self.meshes.append(GraphObject(3))
        # self.grid = Grid2D()  # 2D Intersection grid

        # Camera initialization
        self.cameras = [
            FreeCamera(600, 600),
            SphericalCamera(600, 600),
        ]  # We have both an  oribtal camera and a free camera.
        self.cameras[1].r = 1  # Radius from the origin of the spherical camera

        # FLAGS & Defaults
        self.keep_centered = True
        self.active_camera = CameraType.Free
        self.active_shader = None
        self.dimensionality = 2
        self.active_mesh = 0
        self.fps = 30.0  # Number of times a second we refresh the widget.
        self.DISPLAY_GRID = False

        # DEBUG Flags
        self.DEBUG = False

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1 / self.fps)

    def toggle_camera_type(self):
        self.active_camera = (
            CameraType.Orbital
            if self.active_camera == CameraType.Free
            else CameraType.Free
        )

    # Toggle drawing of debug objects.
    def toggle_debug(self):
        self.DEBUG = not self.DEBUG

    # Toggles displaying the grid over it.
    def toggle_grid(self):
        self.DISPLAY_GRID = not self.DISPLAY_GRID

    # Will return an integer camera type
    def get_camera_type(self):
        return self.active_camera

    # Will accept a CameraType argument(or an integer)
    # 0 = free camera with drag panning
    # 1 = oribtal camera
    def set_camera_type(self, c):
        if self.active_camera != c:
            self.toggle_camera_type()
            self.active_camera = c  # Fuck error checking

    # Do I really need this? Meh. I was feeling it before but now it feels fat.
    def set_dimensions(self, d):
        if d != 2 and d != 3:
            print(
                "[ ERROR ] Dimensionality being set to something other than 2d or 3d."
            )
        self.dimensionality = d
        if d == 2:
            self.active_shader = self.shader2D
            self.active_mesh = 0
            self.clear_graph()
        else:
            self.active_mesh = 1
            self.active_shader = self.shader3D
            self.clear_graph()

    # This is from QOpenGLWidget, this is where all drawing is done.
    def paintGL(self):
        glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Update the camera data
        self.cameras[self.active_camera].update()
        # Upload the updates to both shaders.
        self.cameras[self.active_camera].apply_update(self.shader2D)
        self.cameras[self.active_camera].apply_update(self.shader3D)
        # Update the shader uniform variables.
        glUseProgram(self.shader2D)
        glUniform1f(
            glGetUniformLocation(self.shader2D, "time"), time() - self.start_time
        )
        glUseProgram(self.shader3D)
        glUniform1f(
            glGetUniformLocation(self.shader3D, "time"), time() - self.start_time
        )
        # Draw debug objects
        self.meshes[self.active_mesh].draw()

    # Converts a qt mouse position event coordinates to opengl coordinates
    # aka top left from(0,0) to bottom left being (-1,-1) and top right being (1,1)
    def qt_pos_to_ogl(self, pos):
        # Subtract 1/2 the screen w/h from the pos.
        qpos = np.array([pos.x(), pos.y()])
        wsize = np.array([self.size().width(), self.size().height()])
        return qpos - wsize

    # Not sure if we'll ever need these NDC conversions, but prepping.
    # Converts a mouse position to normalized device coordinates.
    # Assumes the pos is a tuple, list, or np array of size 2.
    def to_normalized_device_coordinates(self, pos):
        wsize = np.array([self.size().width(), self.size().height()])
        return (pos[0] / wsize[0] * 2 - 1, 1 - pos[1] / wsize[1] * 2)

    # Converts a Qt event to normalized device coordinates.
    def qt_pos_to_ndc(self, pos):
        qpos = np.array([pos.x(), pos.y()])
        return self.to_normalized_device_coordinates(qpos)

    def zoom_in(self):
        # if(self.active_camera==CameraType.Orbital):
        self.cameras[1].add_r(-0.2)
        # print("Radius: " + str(self.cameras[self.active_camera].getR()))
        # else:
        self.cameras[0].translate([0, 0, -0.2])
        self.update()

    def zoom_out(self):
        self.cameras[1].add_r(0.2)
        self.cameras[0].translate([0, 0, 0.2])
        self.update()

    # Resets camera to default position & orientation
    def reset_camera(self):
        self.cameras[1].theta = 90
        self.cameras[1].psi = 0
        self.cameras[1].r = 2
        self.cameras[0].set_position([0, 0, 1])
        self.cameras[0].set_orientation([0, 0, 0])
        self.update()

    def mousePressEvent(self, event):
        """ Stores the mouse position when clicked"""
        self.mouse_last_x = event.pos().x()
        self.mouse_last_y = event.pos().y()

    def mouseMoveEvent(self, event):
        """Calculates the movement for panning"""
        # Store current mouse position
        self.mouse_x = event.pos().x()
        self.mouse_y = event.pos().y()

        # Find the mouse delta
        xdiff = self.mouse_last_x - self.mouse_x
        ydiff = self.mouse_last_y - self.mouse_y

        self.mouse_last_x = self.mouse_x
        self.mouse_last_y = self.mouse_y

        if self.active_camera == CameraType.Orbital:
            # Get the radius
            # radius = self.cameras[self.active_camera].getR()

            self.cameras[self.active_camera].addTheta(xdiff)
            self.cameras[self.active_camera].addPsi(ydiff)
        else:
            # Pan around the scene
            movement_speed = 0.01
            trans_vector = np.zeros(3)
            if xdiff != 0:
                trans_vector[0] = -1 if xdiff < 0 else 1
            if ydiff != 0:
                trans_vector[1] = 1 if ydiff < 0 else -1
            trans_vector *= movement_speed

            self.cameras[self.active_camera].translate(trans_vector)
        self.update()

    # Called when the OpenGL widget resizes.
    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0, 0, w, h)
        self.cameras[0].resize(w, h)
        self.cameras[1].resize(w, h)

        # if(self.keep_centered):
        self.center_mesh()

    # Defines whether to keep the mesh centered in the view after resizes.
    def center_on_resize(self, val):
        self.keep_centered = val

    # OpenGL initialization
    def initializeGL(self):
        print("[ INFO ] Initializing OpenGL...")
        # Check for opengl version to be core or es
        gl_version = glGetString(GL_VERSION)
        print("OpenGL Version detected: " + str(gl_version))
        self.load_shaders()
        print("[ INFO ] Shader ID: " + str(self.active_shader))
        self.meshes[0].set_shader(self.active_shader)
        self.meshes[1].set_shader(self.shader3D)

    def load_shaders(self):
        # Load the shader files into a string.
        print("[ INFO ] Loading shaders...")
        with open("assets/shaders/2DShader.vs", "r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/2DShader.fs", "r") as f:
            fc = "".join(f.readlines()[0:])

        print("[ INFO ] Loaded 2D shader code...")
        try:
            # Compile hte shaders on the graphics card.
            self.vs2 = shaders.compileShader(vc, GL_VERTEX_SHADER)
            self.fs2 = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
            # Link them together & compile them as a program.
            self.shader2D = shaders.compileProgram(self.vs2, self.fs2)

        except Exception as err:
            print("[ ERROR ] Caught an exception: " + str(err))
            exit(1)  # Can't proceed without working shaders.

        # 3D Shaders
        with open("assets/shaders/3DShader.vs", "r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/3DShader.fs", "r") as f:
            fc = "".join(f.readlines()[0:])
        print("[ INFO ] Loaded 3D shader code...")
        try:
            # Compile hte shaders on the graphics card.
            self.vs3 = shaders.compileShader(vc, GL_VERTEX_SHADER)
            self.fs3 = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
            # Link them together & compile them as a program.
            self.shader3D = shaders.compileProgram(self.vs3, self.fs3)

        except Exception as err:
            print("[ ERROR ] Caught an exception: " + str(err))
            exit(1)  # Can't proceed without working shaders.
        self.active_shader = self.shader2D
        print("[ INFO ] Shaders loaded to graphics card.")

    # Saves a screenshot of the current OpenGL buffer to a given filename.
    # MUST have a file extension for now.
    def screenshot(self, filename):
        print("[ INFO ] Saving screenshot to " + str(filename) + "...")
        size = self.size()
        pos_x = self.pos().x()  # Starts from the left. Which is fine.
        pos_y = self.pos().y()
        parent = self.parentWidget()
        pheight = parent.size().height()
        pos_y += size.height()
        pos_y = pheight - pos_y

        # Read all of the pixels into an array.
        pixels = glReadPixels(
            pos_x, pos_y, size.width(), size.height(), GL_RGB, GL_UNSIGNED_BYTE
        )
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
        self.clear_graph()
        for m in self.meshes:
            m.cleanup()

        # Detaching shaders and deleting shader program
        # glDetachShader(self.shader, self.vs)
        # glDetachShader(self.shader, self.fs)
        glDeleteShader(self.vs2)

        glDeleteShader(self.fs2)
        glDeleteProgram(self.shader2D)
        glDeleteShader(self.vs3)

        glDeleteShader(self.fs3)
        glDeleteProgram(self.shader3D)

    def center_mesh(self):
        if len(self.graph.vertices) == 0:
            return
        (xmax, ymax), (xmin, ymin) = self.meshes[self.active_mesh].detect_2d_edges()
        xdiff = abs(xmax - xmin)
        ydiff = abs(ymax - ymin)
        scale = max(xdiff, ydiff)
        self.meshes[self.active_mesh].setScale(vec3(1.0 / scale))
        pos = vec3(0.0)
        xmid = (xmax + xmin) / 2.0 * -1
        ymid = (ymax + ymin) / 2.0 * -1
        pos[0] = xmid
        pos[1] = ymid
        self.meshes[self.active_mesh].set_position(pos)

    # # Centers the mesh in the view
    # def center_mesh(self):
    # if (len(self.meshes)==0):
    # return
    # min_x, min_y, max_x, max_y = self.get_extrema()
    # center = ((min_x+max_x)/2, (min_y+max_y)/2)
    # for mesh in self.meshes:
    # mesh.shift_vertices(-0,-center[1])

    # Sets the vertices of the last mesh in the array.
    # split=True creates a new mesh before setting the vertices.
    def set_graph(self, graph):
        self.graph = graph
        self.meshes[self.active_mesh].set_graph_data(graph)
        self.center_mesh()

    # Cleans up the mesh memory on the GPU and clears the array of them.
    def clear_graph(self):
        self.graph.clear()
        self.meshes[0].clear_graph()
        self.meshes[1].clear_graph()

    # Sets the background color of the OpenGL widget.
    def set_bg_color(self, color):
        if len(color) == 4:
            self.bgcolor = np.array(color, dtype=np.float32)
        elif len(color == 3):
            self.bgcolor = np.array(color[0], color[1], color[2], 0.0, dtype=np.float32)
        else:
            print("")
        self.bgcolor = color


if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    l1 = QLabel("Label 1")
    l2 = QLabel("Label 2")
    ogl = LSystemDisplayWidget()
    layout.addWidget(ogl)

    window.setLayout(layout)
    window.show()

    app.exec_()
    ogl.cleanup()
