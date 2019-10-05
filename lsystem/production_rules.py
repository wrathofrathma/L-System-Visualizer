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
