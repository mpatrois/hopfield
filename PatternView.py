import numpy
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

from DrawPattern import drawPattern

class PatternView:
  
  def __init__(self,pattern,nbCol,size=20):
    self.pattern = pattern
    self.nbCol   = nbCol
    self.size    = size

  def drawSteps(self,painter,x,y):
    for idx,step in enumerate(self.pattern.steps):
      xStep =  idx * self.getWidth() + x
      painter.setBrush(QBrush(Qt.white))
      drawPattern(painter,step,xStep+10,y,self.nbCol,self.size)

    self.drawErrorPercentage(painter,x + 10 + len(self.pattern.steps) * self.getWidth(),y + self.getHeight()/2)

  def drawErrorPercentage(self,painter,x,y):
    errorPercentage = self.pattern.errorPercentage(self.pattern.getFirstStep())
    errorTxt = str(errorPercentage) + "%"
    
    path = QPainterPath()
    font = QFont()
    font.setPixelSize(self.size * 1.5)
    path.addText(x,y, font, errorTxt)
    painter.setBrush(QBrush(Qt.blue))
    painter.drawPath(path)

  def getHeight(self):
    return len(self.pattern.original)/self.nbCol * self.size

  def getWidth(self):
    return self.size * self.nbCol + 10