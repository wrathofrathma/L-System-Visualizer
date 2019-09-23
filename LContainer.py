from graphics.Mesh import *

class LContainer():
    def __init__(self):
        self.meshes = []

    def split(self):
        self.meshes.append(Mesh())
        self.meshes[-1].setShader(self.shader)

    def add_vertex(self, vertex):
        print("Adding vertex: " + str(vertex))
        if(len(self.meshes)==0):
            self.meshes.append(Mesh())
            self.meshes[-1].setShader(self.shader)

        vertices = self.meshes[-1].getVertices()
        vertices = np.append(vertices, vertex)
        print(vertices)
        self.meshes[-1].setVertices(vertices)
        print("Post updated vertices: " + str(self.meshes[-1].getVertices()))

    def cleanup(self):
        for mesh in self.meshes:
            mesh.cleanup()

    def draw(self):
        count = 0
        for mesh in self.meshes:
            mesh.draw()
            count+=1

    def setShader(self, shader):
        self.shader = shader
        for mesh in self.meshes:
            mesh.setShader(shader)
