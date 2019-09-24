# -*- coding: utf-8 -*-

from pointer_class import *
from production_rules import *

funcdict = {
  'F': Ff,
  'f':Ff,
  '+': plus,
  '-': minus
}

#l = ['F','f','+','-','F']
def readStack(stack, starting_pt):
  """
  Input list of strings (F, +, -)
  Output List of new vertices 
  """
  vertices = []
  obj = pointer_class(starting_pt[0],starting_pt[1])
  for i in range(len(stack)):
    funcdict[stack[i]](obj)
    vertices.append(obj.pos)
  vertices = list(dict.fromkeys(vertices)) # remove duplicates
  return vertices

