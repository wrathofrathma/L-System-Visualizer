from lsystem.graphics.Camera import *
from lsystem.graphics.OrbitalObject import *

class SphericalCamera(Camera, OrbitalObject):
    def __init__(self, width, height):
        super().__init__()
        self.resize(width, height)

    # updates the view matrix for the current position and line of sight to the origin
    def updateView(self):
        self.view = self.getFacing()

    # Called every draw cycle
    def update(self):
        self.updateView()
