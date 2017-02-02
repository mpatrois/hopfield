import numpy
from DrawPattern import *

class HopfieldMatrixView:
  
  def __init__(self,hopfieldMatrix,nbCol,size=20):
    self.hopfieldMatrix = hopfieldMatrix
    self.nbCol = nbCol
    self.size  = size

  def addDataLearnedToScene(self,scene,x,y):
    for idx,data  in enumerate(self.hopfieldMatrix.datas):
      xStep =  idx * (self.size * self.nbCol + 10) + x
      addPatternToScene(scene,data,xStep+10,y,self.nbCol,self.size)