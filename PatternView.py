import numpy
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

from DrawPattern import *

class PatternView:
  
  def __init__(self,pattern,nbCol,size):
    self.pattern = pattern
    self.nbCol   = nbCol
    self.size    = size

  def drawSteps(self,painter,x,y):
    for idx,step in enumerate(self.pattern.steps):
      xStep =  idx * self.getWidth() + x
      painter.setBrush(QBrush(Qt.white))
      drawPattern(painter,step,xStep+10,y,self.nbCol,self.size)

    self.drawErrorPercentage(painter,x + 10 + len(self.pattern.steps) * self.getWidth(),y + self.getHeight()/2)
    self.drawEnergy(painter,x + 10 + len(self.pattern.steps) * self.getWidth(),y + self.getHeight())

  def addStepsToScene(self,scene,x,y):
    for idx,step in enumerate(self.pattern.steps):
      xStep =  idx * self.getWidth() + x
      addPatternToScene(scene,step,xStep+10,y,self.nbCol,self.size)

    self.addPercentage(scene,x,y)
    self.addEnergy(scene,x,y)
    


  def addPercentage(self,scene,x,y):
    errorPercentage = self.pattern.errorPercentage(self.pattern.getFirstStep())
    errorTxt = 'Erreur :' + str(errorPercentage) + "%"
    xPercentage = x + 10 + len(self.pattern.steps) * self.getWidth()
    yPercentage = y + self.size /2

    addTextToScene(scene,xPercentage,yPercentage,errorTxt,self.size,'red')


  def addEnergy(self,scene,x,y):
    energy = self.pattern.energy()
    energyTxt ='Energie :' + str(energy)
    xEnergy = x + 10 + len(self.pattern.steps) * self.getWidth()
    yEnergy = y + self.getHeight() /2 + self.size /2
    
    addTextToScene(scene,xEnergy,yEnergy,energyTxt,self.size,'blue')

  def getHeight(self):
    return len(self.pattern.original)/self.nbCol * self.size

  def getWidth(self):
    return self.size * self.nbCol + 10