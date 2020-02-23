from graphics.Camera import *
from graphics.QuaternionObject import *

from glm import mat4, translate

class FreeCamera(Camera, QuaternionObject):
    def __init__(self, width, height):
        Camera.__init__(self)
        QuaternionObject.__init__(self)
        self.resize(width, height)
        self.translate([0, 0, 1])
        self.updateView()

    def updateView(self):
        rotation = self.getRotationMatrix()
        translation = mat4(1.0)
        translation = translate(translation, -self.position)
        self.view = rotation * translation

    def update(self):
        self.updateView()
