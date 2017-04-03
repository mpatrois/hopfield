import numpy
import random
import math

class Pattern:
  
  def __init__(self,array,hopfieldMatrix):
    self.original = array
    self.steps    = []
    self.hopfieldMatrix = hopfieldMatrix;

    self.nbNeurons = len(self.original)
    self.rangeNbNeurons = range(self.nbNeurons)


    self.fasSignalTransformation = {
      0:self.add_nothing,
      1:self.add_filter,
      2:self.add_blockage,
      3:self.add_reflection
    }

  def calculAllSteps(self,noisePercentage):
    self.calculAllStepsSync(noisePercentage)

  def calculAllStepsSync(self,noisePercentage):

    weightMatrix = self.hopfieldMatrix.matrix
    matrixFAS = self.hopfieldMatrix.matrixFAS
    data = self.makeNoise(noisePercentage)
    
    start  = numpy.array(data)
    self.steps.append(start)

    lenVector = len(start)


    while(True):
      
      # out = numpy.dot(self.getLastNeuronsState(),weightMatrix) #multiply matrix out by matrixHop
      
      last_neurons_step = numpy.copy(self.getLastNeuronsState())
      new_neurons_state = numpy.zeros((lenVector))

      for i in range(lenVector):
        neuronIActivity = 0
        for j in range(lenVector):
          spikeNeuron = last_neurons_step[j]
          fasType = matrixFAS[i,j]
          spikeNeuron = self.fasSignalTransformation[fasType](spikeNeuron)
          neuronIActivity = neuronIActivity + weightMatrix[i][j] * spikeNeuron
        new_neurons_state[i] = self.transferFunction(neuronIActivity)

      self.steps.append(new_neurons_state)


      if(self.isStable(new_neurons_state) == 1 ):
        break


  def isStable(self,lastStep):
    nbSteps = len(self.steps)
    for i in range(nbSteps):
      if( numpy.all( numpy.sign(self.steps[nbSteps-1-i]) == numpy.sign(lastStep) )):
        if(self.steps[nbSteps-1-i] is not lastStep):
          return True
    
    return False

  def transferFunction(self,number):
    return -1.0 if (number<0) else 1.0

  def add_blockage(self,val):
    return 0

  def add_reflection(self,val):
   return math.floor(0.5 * val)

  def add_filter(self,val):
   return val*0.8
  
  def add_nothing(self,val):
   return val

  def aux_gain_sigmoid(self,val):
    return 0.5 * (1+numpy.tanh(val))


  def signFunction (self,arrayToSign,nbIt):
    sizePattern = len(arrayToSign)
    for i in range(sizePattern):
      
      rand = random.randint(0,2)
      print(rand)

      # if(rand==0):
      arrayToSign[i] = self.add_filter(arrayToSign[i],nbIt)
      # elif (rand==1):
      arrayToSign[i] = self.add_reflection(arrayToSign[i])
      # elif(rand==2):
      #   arrayToSign[i] = self.add_blockage(i)


      arrayToSign[i] =  self.transferFunction(arrayToSign[i])
    
  def recallEfficiency(self):
    nbErrors = 0
    lastStep = self.getLastNeuronsState()

    return int(( numpy.all( numpy.sign(lastStep) == self.original )))
    

  def getLastNeuronsState(self):
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
    array = [i for i in range(int(self.nbNeurons))]
    random.shuffle(array)

    errors = [array.pop() for i in range(int(nbErrorsToMake))]
      
    data = numpy.copy(self.original)

    while len(errors)>0:
      idx = errors.pop()
      if(data[idx] == -1.0):
        data[idx] = 1.0
      else:
        data[idx] = -1.0

    return data

  def makeNoiseLeft(self,noisePercentage):
    nbErrorsToMake = noisePercentage * self.nbNeurons / 100
    array = [i for i in range(int(self.nbNeurons/2))]
    random.shuffle(array)

    errors = [array.pop() for i in range(int(nbErrorsToMake))]
      
    data = numpy.copy(self.original)

    while len(errors)>0:
      idx = errors.pop()
      if(data[idx] == -1.0):
        data[idx] = 1.0
      else:
        data[idx] = -1.0

    return data

  def makeNoiseRight(self,noisePercentage):
    nbErrorsToMake = noisePercentage * self.nbNeurons / 100
    array = [i for i in range(int(self.nbNeurons/2),int(self.nbNeurons/2)*2)]
    random.shuffle(array)

    errors = [array.pop() for i in range(int(nbErrorsToMake))]
      
    data = numpy.copy(self.original)

    while len(errors)>0:
      idx = errors.pop()
      if(data[idx] == -1.0):
        data[idx] = 1.0
      else:
        data[idx] = -1.0

    return data

  def makeNoiseCenter(self,noisePercentage):
    nbErrorsToMake = noisePercentage * self.nbNeurons / 100
    array = [i for i in range(int(self.nbNeurons/2)-int(self.nbNeurons/3),int(self.nbNeurons/2)*2-int(self.nbNeurons/3))]
    random.shuffle(array)

    errors = [array.pop() for i in range(int(nbErrorsToMake))]
      
    data = numpy.copy(self.original)

    while len(errors)>0:
      idx = errors.pop()
      if(data[idx] == -1.0):
        data[idx] = 1.0
      else:
        data[idx] = -1.0

    return data