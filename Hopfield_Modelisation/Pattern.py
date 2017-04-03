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

  def calculAllSteps(self):
    self.calculAllStepsSync()

  def calculAllStepsSync(self):

    weightMatrix = self.hopfieldMatrix.matrix
    matrixFAS = self.hopfieldMatrix.matrixFAS
    
    start  = numpy.copy(self.original)
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


  def recallEfficiency(self):
    nbErrors = 0
    lastStep = self.getLastNeuronsState()

    return int(( numpy.all( numpy.sign(lastStep) == self.original )))