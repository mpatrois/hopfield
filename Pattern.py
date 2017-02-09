import numpy
import random

class Pattern:
  
  def __init__(self,array,hopfieldMatrix,isBinary):
    self.original = array
    self.steps    = []
    self.maxValue = 1.0;
    self.minValue = 0.0 if isBinary else -1.0;
    self.hopfieldMatrix = hopfieldMatrix;

  # def calculAllSteps(self,errorPercentage,typeFunction):

  #   matrixHop = self.hopfieldMatrix.matrix
  #   data = self.makeNoise(errorPercentage)
    
  #   start  = numpy.array(data)
  #   self.steps.append(start)
    
  #   out = numpy.dot(start,matrixHop)
    
  #   for i in range(len(out)):
  #     out[i] =  self.transferFunction(out[i],typeFunction)
          
  #   while( self.isStable(out) == 0 ):
  #     out = numpy.dot(out,matrixHop) #multiply matrix out by matrixHop
  #     for i in range(len(out)):
  #       out[i] =  self.transferFunction(out[i],typeFunction)
  #     self.steps.append(out)

  def calculAllSteps(self,errorPercentage,typeFunction):

    matrixHop = self.hopfieldMatrix.matrix
    data = self.makeNoise(errorPercentage)
    
    start  = numpy.array(data)
    self.steps.append(start)
              
    while(True):
      out = numpy.dot(self.getLastStep(),matrixHop) #multiply matrix out by matrixHop
      
      self.sign(out,typeFunction)
      self.steps.append(out)
      
      if(self.isStable(out) == 1 ):
        break 

  def calculAllStepsAsync(self,errorPercentage,typeFunction):

    matrixHop = self.hopfieldMatrix.matrix
    data = self.makeNoise(errorPercentage)
    
    start  = numpy.array(data)
    self.steps.append(start)

    sequence = [i for i in range(len(self.original))]
    # sequence = [2,1,0]
    sequenceToFollow = numpy.copy(sequence)
    # random.shuffle(sequenceToFollow)

    stepSequences = []
    stop = False
    
    while ( self.isStableAsync(stepSequences,len(self.original) ) == 0 and stop == False):

      stepSequence = []
      out = None
      sequenceToFollow = numpy.copy(sequence).tolist()
      
      while( len(sequenceToFollow) > 0 ):
        lastStep = self.getLastStep()
        out =  numpy.copy(lastStep)
        product = numpy.dot(out,matrixHop) #multiply matrix out by matrixHop
        
        idxToUpdate = sequenceToFollow.pop()
        out[idxToUpdate] = product[idxToUpdate] 

        self.sign(out,typeFunction)
        stepSequence.append(out)

        self.steps.append(out)
      
      stepSequences.append(stepSequence)




  def isStable(self,lastStep):
    for i in range(len(self.steps)):
      if( numpy.all( numpy.sign(self.steps[i]) == numpy.sign(lastStep) )):
        if(self.steps[i] is not lastStep):
          return True
    
    return False

  def isStableAsync(self,stepSequences,nbSteps):
    if(len(stepSequences)>2):
      lastStepSequence = stepSequences[len(stepSequences)-1]
      anteLastStepSequence = stepSequences[len(stepSequences)-2]

      for i in range(len(lastStepSequence)):
        stepsOne = lastStepSequence[i]
        stepsTwo = anteLastStepSequence[i]
        if( numpy.all( numpy.sign(stepsOne) == numpy.sign(stepsTwo) )):
          return True

    else:
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

    return 12

  def sign (self,arrayToSign,typeFunction):
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