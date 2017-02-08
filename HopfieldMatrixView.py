import numpy
from DrawPattern import *
from PatternView import *

class HopfieldMatrixView(QGraphicsView):    

  def __init__(self,hopfieldMatrix,size,mainWindow):
    QGraphicsView.__init__(self)
    
    self.hopfieldMatrix = hopfieldMatrix
    # self.hopfieldMatrix.nbCol = hopfieldMatrix.nbCol
    self.size  = size

    self.scene = QGraphicsScene(self)
    self.setScene(self.scene)

    self.mainWindow = mainWindow

  def addDataLearnedToScene(self):

    patternWidth =  self.size * self.hopfieldMatrix.nbCol
    patternHeight =  self.size * self.hopfieldMatrix.nbRow()

    for idx,data in enumerate(self.hopfieldMatrix.dataToLearn):
      xStep =  idx * (self.size * self.hopfieldMatrix.nbCol + 10)
      addPatternToScene(self.scene,data,xStep,0,self.hopfieldMatrix.nbCol,self.size)
      if(not self.hopfieldMatrix.dataToLearnActived[idx]):
        addRectToScene(self.scene,xStep,0,patternWidth,patternHeight,'black')

  def mousePressEvent(self,event):
    posMouse = self.mapToScene(event.pos())
    indexPattern = self.getIndexOfPattern(posMouse)

    if(indexPattern!=-1):
      self.hopfieldMatrix.dataToLearnActived[indexPattern] = not self.hopfieldMatrix.dataToLearnActived[indexPattern]
      self.mainWindow.update()

  def getIndexOfPattern(self,pos):
    nbPattern = len(self.hopfieldMatrix.dataToLearn)
    patternWidth =  self.size * self.hopfieldMatrix.nbCol
    patternHeight =  self.size * self.hopfieldMatrix.nbRow()
    for idx in range(nbPattern):
      xPattern   = idx * (self.size * self.hopfieldMatrix.nbCol + 10)
      rectPattern = QRect(xPattern,0,patternWidth,patternHeight)
      if(rectPattern.contains(pos.toPoint())):
        return idx

    return -1

  def drawLearnedPatterns(self):
    self.setMinimumHeight(self.size * self.hopfieldMatrix.nbRow() + self.size)
    self.setMaximumHeight(self.size * self.hopfieldMatrix.nbRow() + self.size)

    self.viewport().update()

    self.scene.clear()
    self.addDataLearnedToScene()

  def drawTestedPatterns(self,scenePatterns):
    patternsView = []
    scenePatterns.clear()
    for pattern in self.hopfieldMatrix.patternsTested:
      patternView = PatternView(pattern,self.hopfieldMatrix.nbCol, self.size)
      patternsView.append(patternView)
    
    for patternIndex, patternView in enumerate(patternsView):
      y = patternIndex * ( patternView.getHeight() +  self.size )
      patternView.addStepsToScene(scenePatterns,30,y +  self.size *  self.hopfieldMatrix.nbCol +2* self.size)
