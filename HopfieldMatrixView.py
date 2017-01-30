import numpy
from DrawPattern import drawPattern

class HopfieldMatrixView:
  
  def __init__(self,hopfieldMatrix,nbCol,size=20):
    self.hopfieldMatrix = hopfieldMatrix
    self.nbCol = nbCol
    self.size  = size

  def drawDataLearned(self,painter,x,y):
    for idx,data  in enumerate(self.hopfieldMatrix.datas):
      xStep =  idx * (self.size * self.nbCol + 10) + x
      drawPattern(painter,data,xStep+10,y,self.nbCol,self.size)