# -*- coding: utf-8 -*-

from lsystem.pointer_class import *
from lsystem.production_rules import *
import numpy as np
from time import time
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
#  mesh_arr.append(pointer_class(starting_pt[0],starting_pt[1]))
  trig_dict = dict()
  trig_dict['angle'] = angle
  it =0
  pos_angles= []
  t = time()
  print("[ INFO ] Calculating angles")
  while it < 360:
    pos_angles = np.append(pos_angles,it)
    it+=angle
  sin_arr = np.sin(np.array(pos_angles)*np.pi/180.)
  cos_arr = np.cos(np.array(pos_angles)*np.pi/180.)
  for i in range(len(pos_angles)):
    trig_dict[pos_angles[i]] = (cos_arr[i],sin_arr[i])
  #TODO change pointer class poistion to regular list?
  vertices.append(starting_pt) #append starting position
  new_point = starting_pt
  new_angle = 0
  print("[ INFO ] Finished calcuating angles (",round(time()-t,3),"s )")
  t = time()
  print("[ INFO ] Finding vertices...")
  for i in range(len(s[0])):
    #new_point,new_angle = funcdict[stack[i]](prev_point, prev_angle, trig_dict)
    if s[0][i] == 'F':
      new_point = (new_point[0]+trig_dict[new_angle][0],new_point[1]+trig_dict[new_angle][1])
      vertices.append(new_point)
    elif s[0][i] == '+':
        new_angle = (new_angle - trig_dict['angle'])%360
    elif s[0][i] == '-':
      new_angle = (new_angle + trig_dict['angle'])%360
    #prev_point, prev_angle = new_point, new_angle
#  print(vertices)
  #vertices = list(dict.fromkeys(vertices)) # remove duplicates
  vert_arr.append(vertices)

  #for each little f create a new mesh with the starting position and angle initialized from the previous mesh
  for j in range(1,len(s)):
    vertices = []
    #mesh_arr.append(pointer_class(mesh_arr[-1].pos[0],mesh_arr[-1].pos[1],mesh_arr[-1].angle))
    new_point = (new_point[0]+trig_dict[new_angle][0],new_point[1]+trig_dict[new_angle][1])
    vertices.append(new_point) #append starting position
    for i in range(len(s[j])):
      if s[j][i] == 'F':
        new_point = (new_point[0]+trig_dict[new_angle][0],new_point[1]+trig_dict[new_angle][1])
        vertices.append(new_point)
      elif s[j][i] == '+':
          new_angle = (new_angle - trig_dict['angle'])%360
      elif s[j][i] == '-':
        new_angle = (new_angle + trig_dict['angle'])%360
    #vertices = list(dict.fromkeys(vertices)) # remove duplicates
    vert_arr.append(vertices)
  print("[ INFO ] Finshed finding vertices (",round(time()-t,3),"s )")
  return vert_arr
