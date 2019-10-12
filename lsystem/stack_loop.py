# -*- coding: utf-8 -*-

from lsystem.pointer_class import *
from lsystem.production_rules import *
import numpy as np
from time import time
import copy
import json
funcdict = {
  'F': Ff,
  '+': plus,
  '-': minus
}
#l = ['F','f','+','-','F']
def readsubstring(string, starting_pt, start_angle, trig_dict):
  """
  Input: readsubstring takes in a string, a starking point, the starting angle,
  the dictinary of angles and their trig values and an empty array
  Output: returns angle and vertices
  """
  vertContainer = [] # make sure it's empty
  new_point = starting_pt # initalize starting point
  new_angle = start_angle # initalize starting angle
  vertContainer.append(new_point) # append first point
  for i in range(len(string)):
    if not new_angle in trig_dict.keys():
      trig_dict[new_angle]=[math.cos(new_angle),math.sin(new_angle)]
    if string[i] == 'F':
      new_point = (new_point[0]+trig_dict[new_angle][0],new_point[1]+trig_dict[new_angle][1])
      vertContainer.append(new_point)
    elif string[i] == '+':
        new_angle = round((new_angle - trig_dict['angle'])%360,5)
    elif string[i] == '-':
      new_angle = round((new_angle + trig_dict['angle'])%360,5)
  return new_angle, vertContainer # returns angle that string left off on and array of vertices

def readStack(stack, starting_pt, angle):
  """
  Input list of strings (F, +, -)
  Output List of new vertices
  """
  vertices = []
  vert_arr = []
  mesh_arr =[]
  s = []
  s_temp = stack.split('f')
  saved_states = []
  #keep the delimeter as the first character of the string
  while len(stack)>0:
    indexStartb = stack[1:].find('[') #index of staring bracket
    indexEndb = stack[1:].find(']') #index of end bracket
    indexf = stack[1:].find('f') #index of little f
    if max([indexStartb, indexEndb, indexf]) == -1:
      s.append(stack)
      stack = []
    else:
      nextbreak = min(i for i in [indexStartb, indexEndb, indexf] if i >=0)
      s.append(stack[0:nextbreak+1])
      stack = stack[nextbreak+1:]
  """
  for i in range(1,len(s_temp)):
    s_temp[i]='f'+s_temp[i]
  s.append(s_temp)
  scopy = copy.deepcopy(s)
  s = []
  for t in scopy:
    t = t.split('[')
    for i in range(1,len(t)):
      t[i]='['+t[i]
      s.append(t[i])
  scopy = copy.deepcopy(s)
  s = []
  for t in scopy:
    t = t.split(']')
    for i in range(1,len(t)):
      t[i]=']'+t[i]
      s.append(t[i])
  """
  #Set up a dictionary of all the possible angles and calculate the sin and cos of those angles ahead of time
  #WARNING currently rounding all angles to 5 digits, may not be exact enough
  trig_dict = dict()
  trig_dict['angle'] = angle
  it =0
  pos_angles= []
  t = time()
  print("[ INFO ] Calculating angles")
  if angle != 0:
    while it < 360:
      if it == math.floor(it):
        print(it)
      pos_angles = np.append(pos_angles,round(it,5))
      it+=angle


  #if the angle doesn't divide evenly into 360, find the negative angles mod 360 too
  if it != 360:
    it = 360
    while it > angle:
      it-=angle
      pos_angles = np.append(pos_angles, round(it,5))

  else:
    pos_angles =np.append(pos_angles,0)


  print("angle dictionary = ",pos_angles)
  sin_arr = np.sin(np.array(pos_angles)*np.pi/180.)
  cos_arr = np.cos(np.array(pos_angles)*np.pi/180.)
  for i in range(len(pos_angles)):
    trig_dict[pos_angles[i]] = (cos_arr[i],sin_arr[i])
  new_point = starting_pt #new point initalized to starting point
  curr_state=(starting_pt, 0)
  #for each little f create a new mesh with the starting position and angle initialized from the previous mesh
  for str in s:
    if str[0]=='f':
      #move little f
      if not new_angle in trig_dict.keys():
        trig_dict[new_angle]=[math.cos(new_angle),math.sin(new_angle)]
      curr_state = ((curr_state[0][0]+trig_dict[curr_state[1]][0],curr_state[0][1]+trig_dict[curr_state[1]][1]),currAngle)
      str.replace('f','')
    elif str[0]=='[':
      saved_states.append(curr_state)
      str.replace('[','')
    elif str[0]==']':
      curr_state = saved_states.pop()
      str.replace(']','')

    currAngle,vertices = readsubstring(str,curr_state[0],curr_state[1],trig_dict)
    vert_arr.append(vertices)
    curr_state = (vertices[-1],currAngle)
  print("[ INFO ] Finshed finding vertices (",round(time()-t,3),"s )")
  return vert_arr
