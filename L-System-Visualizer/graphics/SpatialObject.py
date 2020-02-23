from glm import vec3, vec4

class SpatialObject:
    def __init__(self):
        self.position = vec3(0)
        self.orientation = vec3(0)

    def setPosition(self, pos):
        self.position = vec3(pos)

    def getPosition(self):
        return self.position

    def setOrientation(self, o):
        self.orientation = vec3(o)

    def getOrientation(self):
        return self.orientation
