import numpy as np

class pointer_class: 
  #this class holds position and angle
  def __init__(self, x, y):
    pos = np.array([x,y])
    self.init_pos = pos
    self.pos= pos
    self.angle = 0
  def print_info(self):
    print("Position = ",self.pos)
    print("Angle = ",self.angle)
    
