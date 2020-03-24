from math import cos, pi, sin

from glm import lookAt, vec3

from lsystem.graphics.spatial_object import SpatialObject


class OrbitalObject(SpatialObject):
    def __init__(self):
        super().__init__()
        self.r = 2
        self.theta = 0
        self.psi = 0
        self.deg = pi / 180.0
        self.origin = vec3(0)

    def set_position(self, r, theta, psi):
        self.r = r
        self.theta = theta
        self.psi = psi
        self.position = vec3(
            r * cos(psi * self.deg) * cos(theta * self.deg),
            r * sin(psi * self.deg),
            r * cos(psi * self.deg) * sin(theta * self.deg),
        )

    def get_position(self):
        self.position = vec3(
            self.r * cos(self.psi * self.deg) * cos(self.theta * self.deg),
            self.r * sin(self.psi * self.deg),
            self.r * cos(self.psi * self.deg) * sin(self.theta * self.deg),
        )
        return self.position

    def set_origin(self, origin):
        self.origin = vec3(origin)

    def add_theta(self, num):
        self.theta += num
        if self.theta > 360:
            self.theta -= 360
        if self.theta < 0:
            self.theta += 360
        self.set_position(self.r, self.theta, self.psi)

    def add_r(self, num):
        self.r += num
        if self.r < 0.000001:
            self.r = 0.000001
        self.set_position(self.r, self.theta, self.psi)

    def add_psi(self, num):
        self.psi += num
        if self.psi > 90:
            self.psi = 90
        if self.psi < -90:
            self.psi = -90
        self.set_position(self.r, self.theta, self.psi)

    def set_psi(self, num):
        self.psi = num
        if self.psi > 90:
            self.psi = 90
        if self.psi < -90:
            self.psi = -90
        self.set_position(self.r, self.theta, self.psi)

    def set_r(self, num):
        self.r = num
        if self.r < 0.000001:
            self.r = 0.000001
        self.set_position(self.r, self.theta, self.psi)

    def set_theta(self, num):
        self.num = num
        while self.theta > 360:
            self.theta -= 360
        while self.theta < 0:
            self.theta += 360
        self.set_position(self.r, self.theta, self.psi)

    def get_theta(self):
        return self.theta

    def get_r(self):
        return self.r

    def get_psi(self):
        return self.psi

    def get_facing(self):
        eye = vec3(
            self.r * cos(self.psi * self.deg) * cos(self.theta * self.deg),
            self.r * sin(self.psi * self.deg),
            self.r * cos(self.psi * self.deg) * sin(self.theta * self.deg),
        )
        center = self.origin
        up = vec3(0, 1, 0)
        return lookAt(eye, center, up)
