from PyQt4.QtCore import *
from PyQt4.QtGui  import *

def drawPattern(painter,data,x,y,nbCol,size):
    line = 0
    col  = 0
    painter.setBrush(QBrush(Qt.white))
    for i in range(len(data)):
        
        if(i%nbCol==0):
          line += 1
        col = i%nbCol

        xCase = x + col  * size
        yCase = y + line * size

        case = QRect(xCase,yCase,size,size)
        painter.drawRect(case)
        if (data[i] > 0) :
          painter.fillRect(case,Qt.black)
