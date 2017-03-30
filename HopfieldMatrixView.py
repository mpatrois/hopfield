import numpy

from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets  import *




from DrawPattern import *
from PatternView import *

class HopfieldMatrixView():    

  def __init__(self,hopfieldMatrix,size,mainWindow):


    
    
    self.hopfieldMatrix = hopfieldMatrix
    self.size  = size

    self.canvasLearnedData = QGraphicsView()
    self.canvasTestedData = QGraphicsView()

    self.sceneLearnedData = QGraphicsScene(self.canvasLearnedData)
    self.canvasLearnedData.setScene(self.sceneLearnedData)
    self.canvasLearnedData.mousePressEvent = self.mousePressEventCanvasLearnedData

    self.sceneTestedData = QGraphicsScene(self.canvasTestedData)
    self.canvasTestedData.setScene(self.sceneTestedData)

    self.mainWindow = mainWindow


    

  def drawLearnedPatterns(self):

    self.canvasLearnedData.setMinimumHeight(self.size * self.hopfieldMatrix.nbRow() + self.size)
    self.canvasLearnedData.setMaximumHeight(self.size * self.hopfieldMatrix.nbRow() + self.size)
    self.canvasLearnedData.viewport().update()
    self.sceneLearnedData.clear()
    self.canvasLearnedData.viewport().update()

    patternWidth =  self.size * self.hopfieldMatrix.nbCol
    patternHeight =  self.size * self.hopfieldMatrix.nbRow()

    for idx,data in enumerate(self.hopfieldMatrix.dataToLearn):
      xStep =  idx * (self.size * self.hopfieldMatrix.nbCol + 10)
      addPatternToScene(self.sceneLearnedData,data,xStep,0,self.hopfieldMatrix.nbCol,self.size)
      if(not self.hopfieldMatrix.dataToLearnActived[idx]):
        addRectToScene(self.sceneLearnedData,xStep,0,patternWidth,patternHeight,'black')

  def drawTestedPatterns(self):
    patternsView = []
    self.sceneTestedData.clear()
    self.canvasTestedData.viewport().update()

    for pattern in self.hopfieldMatrix.patternsTested:
      patternView = PatternView(pattern,self.hopfieldMatrix.nbCol, self.size)
      patternsView.append(patternView)
    

    
    for patternIndex, patternView in enumerate(patternsView):
      y = patternIndex * ( patternView.getHeight() +  self.size )
      patternView.addStepsToScene(self.sceneTestedData,30,y +  self.size *  self.hopfieldMatrix.nbCol +2* self.size)
      
      

  def mousePressEventCanvasLearnedData(self,event):
    posMouse = self.canvasLearnedData.mapToScene(event.pos())
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


  
