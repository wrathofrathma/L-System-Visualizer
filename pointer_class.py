
class pointer_class: 
  def __init__(self):
    self.position = (0,0)
    self.angle = 0
  def get_angle(self):
    return self.angle
  def get_pos(self):
    return self.position
  def set_angle(self,angle):
    self.angle = angle
  def set_pos(self,pos):
    self.position = pos
  def print_info(self):
    print("Position = ",self.position)
    print("Angle = ",self.angle)
    
