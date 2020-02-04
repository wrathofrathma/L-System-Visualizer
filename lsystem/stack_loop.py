# -*- coding: utf-8 -*-

from lsystem.pointer_class import *
from lsystem.production_rules import *
import numpy as np
from time import time
import copy
import json

#TODO: change tuples return array to lists
#(from [[(x,y),..],[(w,z),...],...] to [[[x,y],..],[[w,z],...],...])
def readsubstring(string, starting_pt, start_angle, turnAngle, trig_dict, scale, lineScale):
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
      new_point = [new_point[0]+(scale*trig_dict[new_angle][0]),new_point[1]+(scale*trig_dict[new_angle][1]), 0]
      vertContainer.append(new_point)
    elif string[i] == 'H':
      new_point = [new_point[0]+(scale*trig_dict[new_angle][0]/2),new_point[1]+(scale*trig_dict[new_angle][1]/2), 0]
      vertContainer.append(new_point)
    elif string[i] == '+':
        new_angle = round((new_angle - trig_dict['angle'])%360,5)
    elif string[i] == '-':
      new_angle = round((new_angle + trig_dict['angle'])%360,5)
    elif string[i] == '|':
      new_angle = round((new_angle+180)%360,5)
    elif string[i] == '(':
      trig_dict['angle'] = round((trig_dict['angle'] - turnAngle)%360,5)
      #new_angle = round((new_angle - turnAngle)%360,5)
    elif string[i] == ')':
      trig_dict['angle']=round((trig_dict['angle'] + turnAngle)%360,5)
      #new_angle = round((new_angle + turnAngle)%360,5)
    elif string[i] == '>':
      scale *= lineScale
    elif string[i] == '<':
      scale /= lineScale
  return new_angle, vertContainer, scale # returns angle that string left off on, array of vertices, and the new angle

def readStack(stack, starting_pt, angle, turnAngle, lineScale):
  """
  Input list of strings (F, +, -)
  Output List of new vertices
  """
  print("angle = ",angle)
  currAngle = 0
  stack = stack.replace("G","F")
  stack = stack.replace("g","f")
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
    indexh = stack[1:].find('h') #index of little h
    if max([indexStartb, indexEndb, indexf, indexh]) == -1:
      s.append(stack)
      stack = []
    else:
      nextbreak = min(i for i in [indexStartb, indexEndb, indexf, indexh] if i >=0)
      s.append(stack[0:nextbreak+1])
      stack = stack[nextbreak+1:]
  #Set up a dictionary of all the possible angles and calculate the sin and cos of those angles ahead of time
  #WARNING currently rounding all angles to 5 digits, may not be exact enough
  trig_dict = dict()
  trig_dict['angle'] = angle
  it =0
  pos_angles= []
  t = time()
  scale = float(1);
  print("[ INFO ] Calculating angles")
  absangle = abs(angle)
  if absangle != 0:
    while it < 360:
      pos_angles = np.append(pos_angles,round(it,5))
      it+=absangle
  #if the angle doesn't divide evenly into 360, find the negative angles mod 360 too
  if it != 360:
    it = 360
    while it > angle:
      it-=angle
      pos_angles = np.append(pos_angles, round(it,5))
  else:
    pos_angles =np.append(pos_angles,0)

  sin_arr = np.sin(np.array(pos_angles)*np.pi/180)
  cos_arr = np.cos(np.array(pos_angles)*np.pi/180)
  for i in range(len(pos_angles)):
    trig_dict[pos_angles[i]] = (cos_arr[i],sin_arr[i])
  new_point = starting_pt #new point initalized to starting point
  curr_state=(starting_pt, 0, scale)
  #for each little f/h create a new mesh with the starting position and angle initialized from the previous mesh
  for str in s:
    if str[0]=='f':
      #move little f
      if not curr_state[1] in trig_dict.keys():
        trig_dict[curr_state[1]]=[math.cos(curr_state[1]),math.sin(curr_state[1])]
      curr_state = ([curr_state[0][0]+(scale*trig_dict[curr_state[1]][0]),curr_state[0][1]+(scale*trig_dict[curr_state[1]][1]), 0],currAngle, scale)
      str.replace('f','')
    elif str[0] == 'h':
      #move little h
      if not curr_state[1] in trig_dict.keys():
        trig_dict[curr_state[1]]=[math.cos(curr_state[1]),math.sin(curr_state[1])]
      curr_state = ([curr_state[0][0]+(scale*trig_dict[curr_state[1]][0]/2),curr_state[0][1]+(scale*trig_dict[curr_state[1]][1]/2), 0],currAngle,  scale)
      str.replace('h','')
    elif str[0]=='[':
      saved_states.append(curr_state)
      str.replace('[','')
    elif str[0]==']':
      curr_state = saved_states.pop()
      str.replace(']','')

    currAngle,vertices, scale = readsubstring(str,curr_state[0],curr_state[1], turnAngle ,trig_dict, scale, lineScale)
    vert_arr.append(vertices)
    curr_state = (vertices[-1],currAngle, scale)
  print("[ INFO ] Finshed finding vertices (",round(time()-t,3),"s )")
  #print("vert_arr = ",vert_arr)
  return vert_arr
