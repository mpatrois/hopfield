import numpy
from PyQt5.QtGui  import *
from PyQt5.QtCore import *

from DrawPattern import *

from PIL import Image
from PIL.ImageQt import ImageQt

class PatternView:
  
  def __init__(self,pattern,nbCol,size):
    self.pattern = pattern
    self.nbCol   = nbCol
    self.size    = size

    img = Image.open('image/arrow.png')
    self.arrowImage = ImageQt(img)
      # we need to hold reference to imgQ, or it will crash
    # self.sceneTestedData.addPixmap(pixMap)

   

  def addStepsToScene(self,scene,x,y):

    
    wPattern = self.getWidth()

    wArrow = self.size * 2
    yArrow = y + self.getHeight()/2 - wArrow / 2

    arrowImgForDispay = self.arrowImage.scaled(wArrow,wArrow,Qt.KeepAspectRatio);
    arrowPixMap = QPixmap.fromImage(arrowImgForDispay)


    

    for idx,step in enumerate(self.pattern.steps):
      xStep =  idx * ( self.getWidth() + wArrow + 10) + x
      addPatternToScene(scene,step,xStep,y,self.nbCol,self.size)
      
      if(idx != len(self.pattern.steps)-1):
       addImageToScene(scene,xStep + wPattern + 5 ,yArrow,arrowPixMap)

    # self.addPercentage(scene,x,y)
    # self.addEnergy(scene,x,y)

  def addPercentage(self,scene,x,y):
    errorPercentage = self.pattern.errorPercentage(self.pattern.original)
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
    return self.size * self.nbCol