from glm import (
    mat4,
    vec3,
    mat4_cast,
    normalize,
    conjugate,
    angleAxis,
    scale,
    translate,
    quat,
)


class SpacialObject:
    def __init__(self):
        self.model_matrix = mat4(1.0)
        self.position = vec3(0.0)
        self.current_scale = vec3(1.0)
        self.orientation = vec3(0.0)

    # Adds a rotation value to our object's rotation.
    # Accepts both numpy array & glm vec3.
    def rotate(self, rotation):
        self.orientation += rotation

    # Returns the current rotation matrix.
    def get_rotation_matrix(self):
        return mat4_cast(self.get_rotation_quat())

    # Returns the current rotation quaternion.
    def get_rotation_quat(self):
        # Generate quaternions based on our yaw pitch and roll.
        qyaw = angleAxis(self.orientation.x, vec3(0, 1, 0))
        qpitch = angleAxis(self.orientation.y, vec3(1, 0, 0))
        qroll = angleAxis(self.orientation.z, vec3(0, 0, 1))
        # Generate total accumulated rotation
        orientation = qroll * qpitch * qyaw
        # Normalize/make it length 1
        return normalize(orientation)

    # Determines what the object's x axis is relative to itself.
    # Returns a vector containing the direction to the x axis.
    def get_x_axis(self):
        rotation = self.get_rotation_quat()
        return conjugate(rotation) * vec3(1, 0, 0)

    # Determines what the object's y axis is relative to itself.
    # Returns a vector containing the direction to the y axis.
    def get_y_axis(self):
        rotation = self.get_rotation_quat()
        return conjugate(rotation) * vec3(0, 1, 0)

    # Returns a vector containing the direction to the z axis.
    def get_z_axis(self):
        rotation = self.get_rotation_quat()
        return conjugate(rotation) * vec3(0, 0, 1)

    def set_position(self, pos):
        self.position = vec3(pos)

    def get_position(self):
        return self.position

    def set_orientation(self, o):
        self.orientation = vec3(o)

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
        transMatrix = translate(mat4(1.0), self.position)
        rotMatrix = self.get_rotation_matrix()
        scaleMatrix = scale(mat4(1.0), self.current_scale)
        self.model_matrix = transMatrix * rotMatrix * scaleMatrix
        return self.model_matrix

    def scale(self, s):
        self.current_scale *= s

    def set_scale(self, s):
        self.current_scale = vec3(s)
