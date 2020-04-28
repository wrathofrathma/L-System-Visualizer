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
    """This class encapsulates an object's transformation data & related methods.

    Attributes:
    model_matrix (mat4): Model matrix representing the model's rotation, scale, and transform.
    position (vec3): Vector representing an object's position.
    current_scale(vec3): Vector representing how to scale an object's model.
    rotation (Rotation): scipy.spatial.transform.Rotation representing the object's rotation.
    """
    def __init__(self):
        """Constructor for the SpatialObject class.
        """
        self.model_matrix = mat4(1.0)
        self.position = vec3(0.0)
        self.current_scale = vec3(1.0)
        self.rotation = R.from_rotvec(np.array([0., 0., 0.]))

    
    def get_rotation(self):
        """Gets the rotation data.

        Return:
        scipy.spatial.transform.Rotation: Object's rotation.
        """
        return self.rotation

    def rotate(self, rotation):
        """Applies a rotation to the model's current rotation.

        Parameters:
        rotation (vec3): Rotational vector to apply to each axis of the model's rotation. (Radians)
        """
        r = R.from_rotvec(np.array(rotation))
        self.rotation = r * self.rotation

    def set_rotation(self, rotation):
        """Sets the rotation of the model.

        Parameters:
        rotation (vec3): Rotational vector to apply to each axis of the model's rotation. (Radians)
        """
        self.rotation = R.from_rotvec(np.array(rotation))

    def set_position(self, pos):
        """Sets the position of the object.

        Parameters:
        pos (vec3): Vector representing the object's new position.
        """
        self.position = vec3(pos)

    def get_position(self):
        """Returns the position of the object.

        Return:
        vec3: Position of the object.
        """
        return self.position

    def translate(self, offset, relative=True):
        """Translates/moves the object in world space.

        Parameters:
        offset (vec3): Vector of the translation/move to apply to the object.
        relative (bool): Boolean for whether to apply this move relative to the object(ex. y applied based on the object's own up vector)
        """
        offset = vec3(offset)
        if relative:
            self.position += self.get_x_axis() * offset.x
            self.position += self.get_y_axis() * offset.y
            self.position += self.get_z_axis() * offset.z
        else:
            self.position += offset

    # Generates and returns the object's current model matrix.
    def generate_model_matrix(self):
        """Generates 2/3 of the object's model matrix. Using translation & scale matrices, but missing rotation.

        Return:
        mat4: Model matrix without the rotation.
        """
        trans_matrix = translate(mat4(1.0), self.position)
        scale_matrix = scale(mat4(1.0), self.current_scale)
        self.model_matrix = trans_matrix * scale_matrix
        return self.model_matrix

    def scale(self, s):
        """Applies a scale to the model's current scale multiplicatively.

        Parameters:
        s (vec3): Vector representing the scale to apply the model.
        """
        self.current_scale *= s

    def set_scale(self, s):
        """Sets the scale of the model.

        Parameters:
        s (vec3): The vector reprsenting the scale to apply to the model.
        """
        self.current_scale = vec3(s)
