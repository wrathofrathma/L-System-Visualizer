# -*- coding: utf-8 -*-

from lsystem.pointer_class import *
from lsystem.production_rules import *

funcdict = {
  'F': Ff,
  '+': plus,
  '-': minus
}
#l = ['F','f','+','-','F']
def readStack(stack, starting_pt, angle):
  """
  Input list of strings (F, +, -)
  Output List of new vertices
  """
  vertices = []
  vert_arr = []
  mesh_arr =[]
  s = stack.split('f')

  #set up the first object (mesh)
  mesh_arr.append(pointer_class(starting_pt[0],starting_pt[1]))

  #TODO change pointer class poistion to regular list?
  vertices.append((mesh_arr[0].pos[0],mesh_arr[0].pos[1])) #append starting position
  for i in range(len(s[0])):
    funcdict[stack[i]](mesh_arr[0], angle)
    vertices.append(mesh_arr[0].pos)
  vertices = list(dict.fromkeys(vertices)) # remove duplicates
  vert_arr.append(vertices)

  #for each little f create a new mesh with the starting position and angle initialized from the previous mesh
  for j in range(1,len(s)):
    vertices = []
    mesh_arr.append(pointer_class(mesh_arr[-1].pos[0],mesh_arr[-1].pos[1],mesh_arr[-1].angle))
    Ff(mesh_arr[-1],angle) #move little f
    vertices.append(mesh_arr[-1].pos) #append starting position
    for i in range(len(s[j])):
      funcdict[stack[i]](mesh_arr[-1], angle)
      vertices.append(mesh_arr[-1].pos)
    vertices = list(dict.fromkeys(vertices)) # remove duplicates
    vert_arr.append([vertices])
  return vert_arr
