import numpy

class Pattern:
  
  def __init__(self,array,isBinary):
    self.data     = array
    self.steps    = []
    self.maxValue = 1;
    self.minValue = 0 if isBinary else -1;

  def calculAllSteps(self,matrixHop):

    start  = numpy.array(self.data)
    self.steps.append(start)
    
    out = numpy.dot(start,matrixHop)
    
    for i in range(len(out)):
      out[i] =  self.transferFunction(out[i],'third')
    
    self.steps.append(out)
      
    while( self.isStable(out) == 0 ):
      out = numpy.dot(out,matrixHop) #multiply matrix out by matrixHop
      for i in range(len(out)):
        out[i] =  self.transferFunction(out[i],'third')
      self.steps.append(out)


  def isStable(self,lastStep):
    for i in range(len(self.steps)):
      if( numpy.all( numpy.sign(self.steps[i]) == numpy.sign(lastStep) )):
        if(self.steps[i] is not lastStep):
          return True
    
    return False

  def transferFunction(self,number,typeFunction):
    if (typeFunction == 'first') :
      return self.minValue if (number<0) else self.maxValue
    elif (typeFunction == 'second'):
      return self.minValue if (number<=0) else self.maxValue
    elif (typeFunction == 'third'):
      if (number<0) :
        return self.minValue
      elif (number>0):
        return self.maxValue
      else :
        return number

