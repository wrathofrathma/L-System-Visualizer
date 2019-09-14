from OpenGL import GL
from OpenGL.GL import shaders
import numpy as np
from graphics.Drawable import *

# OpenGL Mesh class.
# Drawing line by line with thousands of objects would take significantly longer periods of time than just deleting/reallocating memory and uploading a new
# mesh.

class Mesh(Drawable):
    def __init__(self):
        super(Drawable, self).__init__()

    # TODO Fix the framerate on this. Seems to only update when PyQT wants us to.
    def draw(self):
        print("Drawing??")