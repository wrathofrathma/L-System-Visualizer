# Placeholder for future production rule functions
import math
from pointer_class import *
def Ff(obj):
  x,y=obj.get_pos()
  obj.set_pos((x+math.cos(obj.get_angle()),y+math.sin(obj.get_angle())))
def rotation(obj,clockwise):
  if clockwise==1:
    obj.set_angle(obj.get_angle()-math.pi/4)
  else:
    obj.set_angle(obj.get_angle() + math.pi/4)
  
