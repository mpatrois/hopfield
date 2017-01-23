import numpy
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

class PatternView:
  
  def __init__(self,pattern,nbCol,size=20):
    self.pattern = pattern
    self.nbCol   = nbCol
    self.size    = size

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

  def drawSteps(self,painter,x,y):
    for idx,step in enumerate(self.pattern.steps):
      xStep =  idx * (self.size * self.nbCol + 10) + x
      self.drawPattern(painter,step,xStep+10,y)

  def getHeight(self):
    return len(self.pattern.data)/self.nbCol * self.size