from lsystem.graphics.Camera import *
from lsystem.graphics.OrbitalObject import *

class SphericalCamera(Camera, OrbitalObject):
    def __init__(self, width, height):
        Camera.__init__(self)
        OrbitalObject.__init__(self)
        self.resize(width, height)
        self.addTheta(90)
        self.updateView()

    # updates the view matrix for the current position and line of sight to the origin
    def updateView(self):
        self.view = self.getFacing()

    # Called every draw cycle
    def update(self):
        self.updateView()
