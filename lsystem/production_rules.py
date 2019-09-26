# Placeholder for future production rule functions
import math
from lsystem.pointer_class import *

def Ff(obj, angle):
  #input: a pointer_class object
  #output: updates pointer class position
  #seperates the position into coordinates
  x = obj.pos[0]
  y = obj.pos[1]
  #calculate new position
  obj.pos = (x+math.cos(obj.angle),y+math.sin(obj.angle))
  return obj.pos
def plus(obj, angle):
  #input:pointer_class object
  #output: updates pointer class angle clockwise
  obj.angle = obj.angle - angle
  return obj.angle

def minus(obj, angle):
  #input:pointer_class object
  #output: updates pointer class angle counter-clockwise
  obj.angle = obj.angle + angle
  return obj.angle
