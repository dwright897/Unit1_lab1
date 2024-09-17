class Rat:
  def __init__(self, sex, weight):
    self.sex = sex
    self.weight = weight
    self.litters = 0

  def __str__(self):
    pass

  def setWeight(self, other):
    self.weight = other

  def setLitters(self):
    self.litters +=1
    return self.litters

  def __repr__(self):
    return str(self.weight)

  def getWeight(self):
    return self.weight
  
  def getSex(self):
    return self.sex

  def canBreed(self):
    if self.litters<=5:
      return True
    else: 
      return False

  def __lt__ (self, other):
    return self.weight < other.weight

  def __gt__ (self, other):
    return self.weight > other.weight
  
  def __le__(self, other):
    return self.weight <= other.weight
  
  def __ge__(self, other):
    return self.weight >=other.weight
  
  def __eq__(self, other):
    return self.weight == other.weight
