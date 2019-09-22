from graphics.Mesh import *

class LContainer():
    def __init__(self):
        self.meshes = []

    def split(self):
        self.meshes.append(Mesh())

    def add_vertex(self, vertex):
        print("Adding vertex: " + str(vertex))
        if(len(self.meshes)==0):
            self.meshes.append(Mesh())

        vertices = self.meshes[-1].getVertices()
        vertices = np.append(vertices, vertex)
        print(vertices)
        self.meshes[-1].setVertices(vertices)

    def cleanup(self):
        pass

    def draw(self):
        for mesh in self.meshes:
            mesh.draw()
