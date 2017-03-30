from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets  import *

blank_color = QBrush(QColor("#E4485D"))
fill_color  = QBrush(QColor("#34344A"))

def addPatternToScene(scene,data,x,y,nbCol,size):
    line = 0
    col  = 0
   
    for i in range(len(data)):
        
        if(i%nbCol==0 and i != 0):
          line += 1

        col = i%nbCol

        xCase = x + col  * size
        yCase = y + line * size

        case = QRectF(xCase,yCase,size,size)
        case_color = fill_color if data[i] > 0 else blank_color

        scene.addRect(case, QPen(QColor("black")), case_color)


        # addTextToScene(scene,xCase,yCase,str(data[i]),size/2,'white')


def addRectToScene(scene,x,y,w,h,color):
    case = QRectF(x,y,w,h)
    scene.addRect(case, QPen(QColor("black")), QBrush(QColor(color)))

def addTextToScene(scene,x,y,text,size,color):
    
    textItem = QGraphicsTextItem()
    textItem.setPos(x,y)
    textItem.setPlainText(text)

    font = QFont()
    font.setPixelSize(size)
    textItem.setFont(font)

    textItem.setDefaultTextColor(QColor(color))

    scene.addItem(textItem)

def addImageToScene(scene,x,y,pixMap):

    item = scene.addPixmap(pixMap)
    item.setPos(x,y)
    