from graphics.Camera import *
from graphics.OrbitalObject import *


class SphericalCamera(Camera, OrbitalObject):
    def __init__(self, width, height):
        Camera.__init__(self)
        OrbitalObject.__init__(self)
        self.resize(width, height)
        self.add_theta(90)
        self.update_view()

    # updates the view matrix for the current position and line of sight to the origin
    def update_view(self):
        self.view = self.get_facing()

    # Called every draw cycle
    def update(self):
        self.update_view()
