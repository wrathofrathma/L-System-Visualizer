# Placeholder for future production rule functions
import math
from pointer_class import *
def Ff(obj):
  #input: a pointer_class object
  #output: updates pointer class position
  #seperates the position into coordinates
  x = obj.pos[0]
  y = obj.pos[1]
  #calculate new position
  obj.pos = (x+math.cos(obj.angle),y+math.sin(obj.angle))
  return obj.pos
def plus(obj):
  #input:pointer_class object 
  #output: updates pointer class angle clockwise
  obj.angle = obj.angle - math.pi/4
  return obj.angle
def minus(obj):
  #input:pointer_class object 
  #output: updates pointer class angle counter-clockwise
  obj.angle = obj.angle + math.pi/4
  return obj.angle
  