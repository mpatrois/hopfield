import numpy
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

class HopfieldMatrixView:
  
  def __init__(self,hopfieldMatrix,nbCol,size=20):
    self.hopfieldMatrix = hopfieldMatrix
    self.nbCol = nbCol
    self.size  = size

  def drawPattern(self,painter,data,x,y):
    line = 0
    col  = 0
    for i in range(len(data)):
        
        if(i%self.nbCol==0):
          line += 1
        col = i%self.nbCol

        xCase = x + col  * self.size
        yCase = y + line * self.size

        case = QRect(xCase,yCase,self.size,self.size)
        painter.drawRect(case)
        if (data[i] > 0) :
          painter.fillRect(case,Qt.black)

  def drawDataLearned(self,painter,x,y):
    for idx,data  in enumerate(self.hopfieldMatrix.datas):
      xStep =  idx * (self.size * self.nbCol + 10) + x
      self.drawPattern(painter,data,xStep+10,y)