import numpy
import random

class Pattern:
  
  def __init__(self,array,hopfieldMatrix,isBinary):
    self.original = array
    self.steps    = []
    self.maxValue = 1.0;
    self.minValue = 0.0 if isBinary else -1.0;
    self.hopfieldMatrix = hopfieldMatrix;

    self.nbNeurons = len(self.original)
    self.rangeNbNeurons = range(self.nbNeurons)

  def calculAllSteps(self,noisePercentage):
    self.calculAllStepsSync(noisePercentage)

  def calculAllStepsSync(self,noisePercentage):

    matrixHop = self.hopfieldMatrix.matrix
    data = self.makeNoise(noisePercentage)
    
    start  = numpy.array(data)
    self.steps.append(start)
              
    while(True):
      out = numpy.dot(self.getLastStep(),matrixHop) #multiply matrix out by matrixHop
      
      self.signFunction(out)
      self.steps.append(out)
      
      if(self.isStable(out) == 1 ):
        break

  def calculAllStepsAsync(self,noisePercentage):

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

        self.signFunction(out)
        
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

  def transferFunction(self,number):
   return self.firstFunction(number)

  def firstFunction(self,number):
    return self.minValue if (number<0) else self.maxValue

  def secondFunction(self,number):
    return self.minValue if (number<=0) else self.maxValue

  def thirdFunction(self,number):
    if (number<0) :
      return self.minValue
    elif (number>0):
      return self.maxValue
    else :
      return number


  def signFunction (self,arrayToSign):
    for i in range(len(arrayToSign)):
      arrayToSign[i] =  self.transferFunction(arrayToSign[i])
    
  def recallEfficiency(self):
    nbErrors = 0
    lastStep = self.getLastStep()

    return int(( numpy.all( numpy.sign(lastStep) == self.original )))
    

  def getLastStep(self):
    if(self.nbSteps()>0):
      return self.steps[self.nbSteps()-1]

  def getFirstStep(self):
    if(self.nbSteps()>0):
      return self.steps[0]

  def nbSteps(self):
    return len(self.steps)


  def makeNoise(self,noisePercentage):
   return self.makeNoiseStandard(noisePercentage)

  def makeNoiseStandard(self,noisePercentage):
    nbErrorsToMake = noisePercentage * self.nbNeurons / 100
    array = [i for i in range(int(self.nbNeurons/2))]
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

  def makeNoiseLeft(self,noisePercentage):
    nbErrorsToMake = noisePercentage * self.nbNeurons / 100
    array = [i for i in range(int(self.nbNeurons/2))]
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

  def makeNoiseRight(self,noisePercentage):
    nbErrorsToMake = noisePercentage * self.nbNeurons / 100
    array = [i for i in range(int(self.nbNeurons/2),int(self.nbNeurons/2)*2)]
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

  def makeNoiseCenter(self,noisePercentage):
    nbErrorsToMake = noisePercentage * self.nbNeurons / 100
    array = [i for i in range(int(self.nbNeurons/2)-int(self.nbNeurons/3),int(self.nbNeurons/2)*2-int(self.nbNeurons/3))]
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