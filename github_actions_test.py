from math import sqrt

class Point():
  def __init__(self,x_value:int,y_value:int):
    self.x = x_value
    self.y = y_value

  def get_values(self):
    return (self.x,self.y)

  def calculate_distance(self,a:Point):
    a_x,a_y = a.get_values()
    return sqrt((x-a_x)**2 + (y-a_y)**2)
