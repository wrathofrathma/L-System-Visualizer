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
from pyqtgraph.opengl import GLViewWidget, GLMeshItem, GLLinePlotItem

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

# from graphics.graph_mesh import GraphObject
from lsystem.graph import Graph

# Other includes
import numpy as np


class CameraType:
    Free = 0
    Orbital = 1


class LSystemDisplayWidget(GLViewWidget):
    def __init__(self):
        super(LSystemDisplayWidget, self).__init__()
        self.start_time = time()

        # Production scene objects.
        self.graph = Graph()
        self.mesh = None

        self.dimensionality = 2
        self.active_mesh = 0
        self.fps = 30.0  # Number of times a second we refresh the widget.

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1 / self.fps)

    # Do I really need this? Meh. I was feeling it before but now it feels fat.
    def set_dimensions(self, d):
        if d != 2 and d != 3:
            print(
                "[ ERROR ] Dimensionality being set to something other than 2d or 3d."
            )
        self.dimensionality = d
        if d == 2:
            self.active_mesh = 0
            self.clear_graph()
        else:
            self.active_mesh = 1
            self.clear_graph()

    def get_camera_type(self):
        return 0

    def set_camera_type(self, c):
        pass

    def reset_camera(self):
        pass

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

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
        pass

    def set_graph(self, graph):
        if self.dimensionality == 2:
            self.set_2dgraph(graph)
        elif self.dimensionality == 3:
            self.set_3dgraph(graph)
        else:
            print("????")
            exit(1)

    # Sets the vertices of the last mesh in the array.
    # split=True creates a new mesh before setting the vertices.
    def set_2dgraph(self, graph):
        self.graph = graph
        # (verts, colors, indices) = graph_to_ogl(graph)
        verts = self.graph.export_to_ogl_verts()
        self.mesh = GLLinePlotItem(
            pos=verts, color=(1, 1, 1, 1), width=1.0, antialias=False, mode="lines"
        )
        self.addItem(self.mesh)

    # 3D Version using GLMeshItem instead of GLLinePlotItem
    def set_3dgraph(self, graph):
        pass

    # Cleans up the mesh memory on the GPU and clears the array of them.
    def clear_graph(self):
        if isinstance(self.mesh, GLLinePlotItem):
            self.removeItem(self.mesh)
        elif isinstance(self.mesh, GLMeshItem):
            self.removeItem(self.mesh)
        self.mesh = None


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
