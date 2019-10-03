# This will someday be a camera class for moving around the scene.

import numpy as np
import glm # from pyglm, not glm
from OpenGL.GL import *

class Camera:
    def __init__(self,width=800, height=600, fov=50.0):
        self.width = width
        self.height = height
        self.FoV = fov
        self.clip_near = 0.1
        self.clip_far = 200.0

        self.view = glm.mat4(0)
        self.projection = glm.mat4(0)

        self.updateProjection()

    def updateProjection(self):
        self.projection = glm.perspective(glm.radians(self.FoV), self.width/ self.height, self.clip_near, self.clip_far)

    def getView(self):
        return self.view

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.updateProjection()

    def applyUpdate(self, shader):
        glUseProgram(shader)
        glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, glm.value_ptr(self.view))
        glUniformMatrix4fv(glGetUniformLocation(shader, "proj"), 1, GL_FALSE, glm.value_ptr(self.projection))
        print("View & Proj matrices")
        print(self.view)
        print(self.projection)
        # Comment out later for lighting calcs.
        #glUniformMatrix4fv(glGetUniformLocation(shader, "camera_pos"), 1, GL_FALSE, glm.value_ptr(self.position))
        glUseProgram(0)
