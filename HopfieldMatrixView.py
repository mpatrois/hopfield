import numpy
from DrawPattern import *

class HopfieldMatrixView(QGraphicsView):    

  def __init__(self,hopfieldMatrix,size,mainWindow):
    QGraphicsView.__init__(self)
    
    self.hopfieldMatrix = hopfieldMatrix
    self.nbCol = hopfieldMatrix.nbCol
    self.size  = size

    self.scene = QGraphicsScene(self)
    self.setScene(self.scene)

    self.mainWindow = mainWindow

  def addDataLearnedToScene(self):

    patternWidth =  self.size * self.nbCol
    patternHeight =  self.size * self.hopfieldMatrix.nbRow()

    for idx,data in enumerate(self.hopfieldMatrix.datas):
      xStep =  idx * (self.size * self.nbCol + 10)
      addPatternToScene(self.scene,data,xStep,0,self.nbCol,self.size)
      if(not self.hopfieldMatrix.datasActived[idx]):
        addRectToScene(self.scene,xStep,0,patternWidth,patternHeight,'black')

  def mousePressEvent(self,event):
    posMouse = self.mapToScene(event.pos())
    indexPattern = self.getIndexOfPattern(posMouse)

    if(indexPattern!=-1):
      self.hopfieldMatrix.datasActived[indexPattern] = not self.hopfieldMatrix.datasActived[indexPattern]
      self.mainWindow.update()

  def getIndexOfPattern(self,pos):
    nbPattern = len(self.hopfieldMatrix.datas)
    patternWidth =  self.size * self.nbCol
    patternHeight =  self.size * self.hopfieldMatrix.nbRow()
    for idx in range(nbPattern):
      xPattern   = idx * (self.size * self.nbCol + 10)
      rectPattern = QRect(xPattern,0,patternWidth,patternHeight)
      if(rectPattern.contains(pos.toPoint())):
        return idx

    return -1

  def drawLearnedPatterns(self):
    self.scene.clear()
    self.addDataLearnedToScene()