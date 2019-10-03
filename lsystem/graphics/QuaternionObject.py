# This file contains the quaternion class, which will be used for all scaling, rotation, and positional components of objects in a scene.

from glm import mat4, vec3, mat4_cast, normalize, conjugate, angleAxis, scale, translate, quat
class QuaternionObject:
    def __init__(self):
        self.model_matrix = mat4(1.0)
        self.position = vec3(0.0)
        self.current_scale = vec3(1.0)
        self.orientation = vec3(0.0)

    # Adds a rotation value to our object's rotation.
    # Accepts both numpy array & glm vec3.
    def rotate(self, rotation):
        self.orientation+=rotation

    # Returns the current rotation matrix.
    def getRotationMatrix(self):
        return mat4_cast(self.getRotationQuat())

    # Returns the current rotation quaternion.
    def getRotationQuat(self):
        # Generate quaternions based on our yaw pitch and roll.
        qyaw = angleAxis(self.orientation.x, vec3(0,1,0))
        qpitch = angleAxis(self.orientation.y, vec3(1,0,0))
        qroll = angleAxis(self.orientation.z, vec3(0,0,1))
        # Generate total accumulated rotation
        orientation = qroll * qpitch * qyaw
        # Normalize/make it length 1
        return normalize(orientation)

    # Determines what the object's x axis is relative to itself.
    # Returns a vector containing the direction to the x axis.
    def getXAxis(self):
        rotation = self.getRotationQuat()
        return conjugate(rotation) * vec3(1,0,0)
    # Determines what the object's y axis is relative to itself.
    # Returns a vector containing the direction to the y axis.
    def getYAxis(self):
        rotation = self.getRotationQuat()
        return conjugate(rotation) * vec3(0,1,0)    # Determines what the object's z axis is relative to itself.
    # Returns a vector containing the direction to the z axis.
    def getZAxis(self):
        rotation = self.getRotationQuat()
        return conjugate(rotation) * vec3(0,0,1)

    # Translates the object according to the passed vector.
    # offset - Vector containing direction to translate our object. Accepted types are numpy array, glm::vec3, and python list with 3 floats.
    def translate(self, offset, relative=True):
        offset = vec3(offset) # making sure we're using a vec3. It is fine for python lists, numpy arrays, and glm::vec3
        if(relative):
            self.position+=self.getXAxis() * offset.x
            self.position+=self.getYAxis() * offset.y
            self.position+=self.getZAxis() * offset.z
        else:
            self.position+=offset

    # Generates and returns the object's current model matrix.
    def generateModelMatrix(self):
        transMatrix = translate(mat4(1.0), self.position)
        rotMatrix = self.getRotationMatrix()
        scaleMatrix = scale(mat4(1.0), self.current_scale)
        self.model_matrix = transMatrix * rotMatrix * scaleMatrix
        return mat4(1)
        #return self.model_matrix

    def scale(self,s):
        self.current_scale*=s
