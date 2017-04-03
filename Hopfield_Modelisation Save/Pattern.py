import numpy
import random

class Pattern:
  
  def __init__(self,array,hopfieldMatrix,isBinary):
    self.original = array
    self.steps    = []
    self.maxValue = 1.0;
    self.minValue = 0.0 if isBinary else -1.0;
    self.hopfieldMatrix = hopfieldMatrix;

  def calculAllSteps(self,noisePercentage,typeFunction):

    matrixHop = self.hopfieldMatrix.matrix
    data = self.makeNoise(noisePercentage)
    
    start  = numpy.array(data)
    self.steps.append(start)
              
    while(True):
      out = numpy.dot(self.getLastStep(),matrixHop) #multiply matrix out by matrixHop
      
      self.signFunction(out,typeFunction)
      self.steps.append(out)
      
      if(self.isStable(out) == 1 ):
        break 

  def calculAllStepsAsync(self,noisePercentage,typeFunction):

    matrixHop = self.hopfieldMatrix.matrix
    data = self.makeNoise(noisePercentage)
    
    start  = numpy.array(data)
    self.steps.append(start)

    sequence = [i for i in range(len(self.original))]
    # sequence = [2,1,0]
    sequenceToFollow = numpy.copy(sequence)

    stop = False
    
    nbPasTotal = -1
    while (stop == False):

      out = None
      sequenceToFollow = numpy.copy(sequence).tolist()
      nbPasSequence = 0
      
      while( len(sequenceToFollow) > 0 and  stop == False ):
        lastStep = self.getLastStep()
        out =  numpy.copy(lastStep)
        product = numpy.dot(out,matrixHop) #multiply matrix out by matrixHop
        
        idxToUpdate = sequenceToFollow.pop()
        out[idxToUpdate] = product[idxToUpdate] 

        self.signFunction(out,typeFunction)
        
        nbPasSequence = nbPasSequence + 1
        nbPasTotal = nbPasTotal + 1

        stepToCompare = nbPasTotal - len(sequence)

        arrayToCompare = []
        
        if( stepToCompare >= 0 ):
          arrayToCompare = self.steps[stepToCompare]

          if( numpy.all( numpy.sign(out) == numpy.sign(arrayToCompare) )):
            stop = True
        
        if(not stop):
          self.steps.append(out)


  def isStable(self,lastStep):
    nbSteps = len(self.steps)
    for i in range(nbSteps):
      if( numpy.all( numpy.sign(self.steps[nbSteps-1-i]) == numpy.sign(lastStep) )):
        if(self.steps[nbSteps-1-i] is not lastStep):
          return True
    
    return False

  def transferFunction(self,number,typeFunction):

    # number =  0.5 * (1+numpy.tanh(number))

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

    return 12

  def signFunction (self,arrayToSign,typeFunction):
    for i in range(len(arrayToSign)):
      arrayToSign[i] =  self.transferFunction(arrayToSign[i],typeFunction)

  def errorPercentage(self,wantedData):
    nbErrors = 0
    lastStep = self.getLastStep()

    if(lastStep is not None):
      for i in range(len(lastStep)):
        if(lastStep[i]!=wantedData[i]):
          nbErrors += 1
      
    return (nbErrors*100)/len(wantedData)

  def energy(self):
    nbErrors = 0
    lastStep  = self.getLastStep()
    firstStep = self.getFirstStep()

    matrixHop = self.hopfieldMatrix.matrix

    length = len(self.original)
    result = 0
    for i in range(length):
      for j in range(length):
        result += lastStep[i]*lastStep[j]*matrixHop[i][j]

    return (-1/2)*result
    

  def getLastStep(self):
    if(self.nbSteps()>0):
      return self.steps[self.nbSteps()-1]

  def getFirstStep(self):
    if(self.nbSteps()>0):
      return self.steps[0]

  def nbSteps(self):
    return len(self.steps)


  def makeNoise(self,noisePercentage):
    nbErrorsToMake = noisePercentage * len(self.original) / 100
    array = [i for i in range(len(self.original))]
    random.shuffle(array)

    errors = [array.pop() for i in range(int(nbErrorsToMake))]
      
    data = numpy.copy(self.original)

    while len(errors)>0:
      idx = errors.pop()
      if(data[idx] == self.minValue):
        data[idx] = self.maxValue
      else:
        data[idx] = self.minValue

    return data