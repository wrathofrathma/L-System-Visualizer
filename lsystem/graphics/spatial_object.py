from glm import (
    mat4,
    mat3,
    vec3,
    vec4,
    mat4_cast,
    normalize,
    conjugate,
    angleAxis,
    scale,
    translate,
)
import numpy as np
from scipy.spatial.transform import Rotation as R


class SpatialObject:
    def __init__(self):
        self.model_matrix = mat4(1.0)
        self.position = vec3(0.0)
        self.current_scale = vec3(1.0)
        self.rotation = R.from_rotvec(np.array([0., 0., 0.]))

    
    def get_rotation(self):
        return self.rotation

    def rotate(self, rotation):
        """applies a rotation using radians"""
        r = R.from_rotvec(np.array(rotation))
        self.rotation = r * self.rotation

    def set_rotation(self, rotation):
        """Sets our rotation in radians."""
        self.rotation = R.from_rotvec(np.array(rotation))

    def set_position(self, pos):
        self.position = vec3(pos)

    def get_position(self):
        return self.position

    def translate(self, offset, relative=True):
        offset = vec3(offset)
        if relative:
            self.position += self.get_x_axis() * offset.x
            self.position += self.get_y_axis() * offset.y
            self.position += self.get_z_axis() * offset.z
        else:
            self.position += offset

    # Generates and returns the object's current model matrix.
    def generate_model_matrix(self):
        trans_matrix = translate(mat4(1.0), self.position)
        scale_matrix = scale(mat4(1.0), self.current_scale)
        self.model_matrix = trans_matrix * scale_matrix
        return self.model_matrix

    def scale(self, s):
        self.current_scale *= s

    def set_scale(self, s):
        self.current_scale = vec3(s)
