from glm import vec3, vec4


class SpatialObject:
    def __init__(self):
        self.position = vec3(0)
        self.orientation = vec3(0)

    def set_position(self, pos):
        self.position = vec3(pos)

    def get_position(self):
        return self.position

    def set_orientation(self, o):
        self.orientation = vec3(o)

    def get_orientation(self):
        return self.orientation
