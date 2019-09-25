import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GLU import *
import numpy as np
from graphics.Mesh import *
from OpenGL.arrays import ArrayDatatype, vbo
from OpenGL.GL import shaders

pygame.init()
pygame.display.set_caption("Hello world")

screen = pygame.display.set_mode((640,480), DOUBLEBUF|OPENGL)


with open("assets/shaders/Default.vs","r") as f:
    vc = "".join(f.readlines()[0:])
with open("assets/shaders/Default.fs","r") as f:
    fc = "".join(f.readlines()[0:])

# Load shaders
shader = shaders.compileProgram(shaders.compileShader(vc, GL_VERTEX_SHADER), shaders.compileShader(fc, GL_FRAGMENT_SHADER))

# Load mesh
vertices = np.array([
    0.0,0.0,
    0.1,0.0], dtype=np.float32)
mesh = Mesh()
mesh.set_vertices(vertices)
mesh.set_shader(shader)
running = True
while(running):
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0,0.0,0,0)
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            running = False
        elif(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_ESCAPE):
                running=False
    # mesh.draw()
    glBegin(GL_LINES)
    glVertex3fv((0.0,0.0,0.0))
    glVertex3fv((0.1,0.0,0.0))
    glEnd()
    pygame.display.flip()

pygame.quit()
