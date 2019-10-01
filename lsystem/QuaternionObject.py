# This file contains the quaternion class, which will be used for all scaling, rotation, and positional components of objects in a scene.

import numpy as np
import quaternion
class QuaternionObject:
    def __init__(self):
        self.model_matrix = np.asmatrix(np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]))
        self.position = np.zeros(3)
        self.current_scale = np.ones(3)
        self.orientation = np.zeros(0)

    def rotate(self, rotation):
        self.orientation+=rotation

    def getRotationMatrix(self):
        pass

    def getRotationQuat(self):
        pass

    def getXAxis(self):
        pass

    def getYAxis(self):
        pass

    def getZAxis(self):
        pass

    def translate(self):
        pass

    def generateModelMatrix(self):
        pass

    def scale(self,s):
        self.current_scale*=s
