# Placeholder for future production rule functions
import math
from lsystem.pointer_class import *

def Ff(pos,prev_angle, trig_dict):
  #input: a pointer_class object
  #output: updates pointer class position
  #seperates the position into coordinates
  x = pos[0]
  y = pos[1]
  #calculate new position
  pos = (x+trig_dict[prev_angle][0],y+trig_dict[prev_angle][1])
  return pos, prev_angle

def Hh(pos,prev_angle, trig_dict):
  #input: a pointer_class object
  #output: updates pointer class position
  #seperates the position into coordinates
  x = pos[0]
  y = pos[1]
  #calculate new position
  pos = (x+(trig_dict[prev_angle][0]/2),y+(trig_dict[prev_angle][1]/2))
  print(pos)
  return pos, prev_angle

def plus(pos,prev_angle, trig_dict):
  #input:pointer_class object
  #output: updates pointer class angle clockwise
  prev_angle = (prev_angle - trig_dict['angle'])%360
  return pos,prev_angle

def minus(pos,prev_angle, trig_dict):
  #input:pointer_class object
  #output: updates pointer class angle counter-clockwise
  prev_angle = (prev_angle + trig_dict['angle'])%360
  return pos,prev_angle

def pipeline(pos, prev_angle, trig_dict):
  #input: pointer_class object
  #output: updates pointer class to go in the opposite direction
  prev_angle = (prev_angle + 180)%360
  trig_dict['angle'] = prev_angle
  it =0
  pos_angles= []
  if prev_angle != 0:
    while it < 360:
      pos_angles = np.append(pos_angles,round(it,5))
      it+=prev_angle
      #if the angle doesn't divide evenly into 360, find the negative angles mod 360 too
    if it != 360:
      it = 360
      while it > prev_angle:
        it-=prev_angle
        pos_angles = np.append(pos_angles, round(it,5))
  else:
    pos_angles =np.append(pos_angles,0)
    
  sin_arr = np.sin(np.array(pos_angles)*np.pi/180.)
  cos_arr = np.cos(np.array(pos_angles)*np.pi/180.)
  for i in range(len(pos_angles)):
    trig_dict[pos_angles[i]] = (cos_arr[i],sin_arr[i])
  return pos,prev_angle,trig_dict

