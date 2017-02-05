#!/usr/bin/env python
#-*- coding:utf-8 -*-

# from PyQt4 import QtCore, QtGui

# class MyDialog(QtGui.QDialog):
#     def __init__(self, parent=None):
#         super(MyDialog, self).__init__(parent)

#         self.buttonBox = QtGui.QDialogButtonBox(self)
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

#         self.textBrowser = QtGui.QTextBrowser(self)
#         self.textBrowser.append("This is a QTextBrowser!")

#         self.verticalLayout = QtGui.QVBoxLayout(self)
#         self.verticalLayout.addWidget(self.textBrowser)
#         self.verticalLayout.addWidget(self.buttonBox)

# class MyWindow(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(MyWindow, self).__init__(parent)

#         self.pushButtonWindow = QtGui.QPushButton(self)
#         self.pushButtonWindow.setText("Click Me!")
#         self.pushButtonWindow.clicked.connect(self.on_pushButton_clicked)

#         self.layout = QtGui.QHBoxLayout(self)
#         self.layout.addWidget(self.pushButtonWindow)

#         self.dialogTextBrowser = MyDialog(self)

#     @QtCore.pyqtSlot()
#     def on_pushButton_clicked(self):
#         self.dialogTextBrowser.exec_()


# if __name__ == "__main__":
#     import sys

#     app = QtGui.QApplication(sys.argv)
#     app.setApplicationName('MyWindow')

#     main = MyWindow()
#     main.show()

#     sys.exit(app.exec_())



    

# import sys
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *


# data = {'col1':['','',''], 'col2':['','',''], 'col3':['','','']}
 
# class MyTable(QTableWidget):
#     def __init__(self, data, *args):
#         QTableWidget.__init__(self, *args)
#         self.data = data
#         self.setmydata()
#         self.resizeColumnsToContents()
#         self.resizeRowsToContents()
#         self.verticalHeader().hide();
#         self.horizontalHeader().hide();
#         self.setFixedSize(self.horizontalHeader().length(), self.verticalHeader().length());

#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
 
#     def setmydata(self):
#         for n, key in enumerate(sorted(self.data.keys())):
#             print(key)
#             for m, item in enumerate(self.data[key]):
#                 newitem = QTableWidgetItem(item)
#                 newitem.setBackground(QColor(100,100,150))
#                 newitem.setFlags(Qt.NoItemFlags)
#                 self.setItem(m, n, newitem)

#         # self.setItem(0,1,QTableWidgetItem(str(237)))

# class Example(QWidget):
    
#     def __init__(self):
#         super(Example, self).__init__()
        
#         self.initUI()
        
#     def initUI(self):
        
#         title = QLabel('Title')
#         author = QLabel('Author')
#         review = QLabel('Review')

#         titleEdit = QLineEdit()
#         authorEdit = QLineEdit()
#         reviewEdit = QTextEdit()

#         table  = MyTable(data, 5, 5)
#         table2 = MyTable(data, 5, 5)
#         table3 = MyTable(data, 5, 5)
#         # table = MyTable(data, 1, 3)
       

#         grid = QGridLayout()
#         grid.setSpacing(0)

#         grid.addWidget(table, 0, 0)
#         grid.addWidget(table2, 0, 1)
#         grid.addWidget(table3, 0, 2)

#         # grid.addWidget(title, 1, 0)
#         # grid.addWidget(titleEdit, 1, 1)

#         # grid.addWidget(author, 2, 0)
#         # grid.addWidget(authorEdit, 2, 1)

#         # grid.addWidget(review, 3, 0)
#         # grid.addWidget(reviewEdit, 3, 1, 5, 1)
        
#         self.setLayout(grid) 
        
#         self.setGeometry(300, 300, 350, 300)
#         self.setWindowTitle('Review')    
#         self.show()
        
# def main():
    
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())


# if __name__ == '__main__':
#     main()
#     
#     

# from PyQt4 import QtGui

# class Window(QtGui.QWidget):
#     def __init__(self, val):
#         QtGui.QWidget.__init__(self)
#         mygroupbox = QtGui.QGroupBox('this is my groupbox')
#         myform = QtGui.QFormLayout()
#         labellist = []
#         combolist = []
#         for i in range(val):
#             labellist.append(QtGui.QLabel('mylabel'))
#             combolist.append(QtGui.QComboBox())
#             myform.addRow(labellist[i],combolist[i])
#         mygroupbox.setLayout(myform)
#         scroll = QtGui.QScrollArea()
#         scroll.setWidget(mygroupbox)
#         scroll.setWidgetResizable(True)
#         scroll.setFixedHeight(400)
#         layout = QtGui.QVBoxLayout(self)
#         layout.addWidget(scroll)

# if __name__ == '__main__':

#     import sys
#     app = QtGui.QApplication(sys.argv)
#     window = Window(25)
#     window.setGeometry(500, 300, 300, 400)
#     window.show()
#     sys.exit(app.exec_())
#     
#     
# import sys
# from PyQt4 import QtGui, QtCore
# class MainFrame(QtGui.QMainWindow):
#     def __init__(self):
#         QtGui.QMainWindow.__init__(self)
#         self.setWindowTitle("Window title") # title
#         self.resize(1024, 768) # size
#         self.setMinimumSize(800, 600) # minimum size
#         self.move(0, 0) # position window frame at top left
#         # Adding the icon:
#         self.setWindowIcon(QtGui.QIcon("myicon.png"))
#        # Set the central widget for the main window
#         cwidget = QtGui.QWidget(self)
#         # Set up a layout for the button and canvas:
#         layout = QtGui.QVBoxLayout() #vertical box layout
#         #layout = QtGui.QHBoxLayout() #horizontal box layout
#         self.add_button(layout)
#         self.add_canvas(layout)
#         cwidget.setLayout(layout)
#         self.setCentralWidget(cwidget)
#         # Now set up the shapes that we draw on each button click
#         # get the button back from the layout
#         button = layout.itemAt(0).widget()
    
#         # Create objects used for drawing
#         sol_pen =  QtGui.QPen(QtGui.QColor("black"))
        
#         dot_pen =  QtGui.QPen(QtGui.QColor("black"))
#         dot_pen.setStyle(QtCore.Qt.DotLine)
#         dash_pen = QtGui.QPen(QtGui.QColor("black"))
#         dash_pen.setStyle(QtCore.Qt.DashLine)
        
#         r_brush = QtGui.QBrush(QtGui.QColor("red"))
#         g_brush = QtGui.QBrush(QtGui.QColor("green"))
#         b_brush = QtGui.QBrush(QtGui.QColor("blue"))
#         triangle = QtGui.QPolygonF()
#         triangle.append(QtCore.QPointF(100, 50))
#         triangle.append(QtCore.QPointF(200, 200))
#         triangle.append(QtCore.QPointF(0, 200))
#         self.scene_data = []
#         # add data for drawing circle
#         #self.scene.addEllipse(0, 0, 150, 150, sol_pen, r_brush) #x, y, w, h etc
#         self.scene_data.append({'routine':self.scene.addEllipse,
#                                 'args':(0,0,150,150,sol_pen,r_brush),
#                                 'z': 0, #z-index
#                                 'next': "Draw Rectangle"})
#         # add data for drawing square
#         #self.scene.addRect(100, 100, 150, 150, dot_pen, g_brush) #x, y, w, h etc
#         self.scene_data.append({'routine':self.scene.addRect,
#                                 'args':(100,100,150,150, dot_pen, g_brush),
#                                 'z':1,
#                                 'next': "Draw Triangle."})
#         # add data for drawing triangle
#         #self.scene.addPolygon(triangle, dash_pen, b_brush)
#         self.scene_data.append({'routine':self.scene.addPolygon,
#                                 'z':2,
#                                 'args':(triangle, dash_pen, b_brush)})
#         # Set up self.draw_next_item to fire when button is clicked.
#         self.connect(button, QtCore.SIGNAL("clicked()"), self.draw_next_item)
       
#     def add_button(self, layout):
#         """Create a button and then add it to the layout."""
#         button = QtGui.QPushButton("Draw Circle")
#         layout.addWidget(button)
#     def add_canvas(self, layout):
#         """Create a canvas and then add it to the layout."""
#         canvas = QtGui.QGraphicsView()
#         layout.addWidget(canvas)
#         # Now create a graphics scene to draw shapes to.
#         # Now remember to keep a reference to GraphicsScene for as long as
#         # you're using it, because unlike widgets, these are automatically
#         # destroyed when they lose reference count
#         self.scene = QtGui.QGraphicsScene()
#         canvas.setScene(self.scene)
#     def draw_next_item(self):
#         # get the button. could've just saved as self.button, but I wanted to
#         # show how it could be done this way
#         button = self.centralWidget().layout().itemAt(0).widget()
#         d = self.scene_data.pop(0) # get first item
#         item = d['routine'](*d['args']) # just a little python magic
#         item.setZValue(d['z'])
#         if len(self.scene_data):
#             # more stuff to draw, set button label
#             button.setText(d['next'])
#         else:
#             # no more left, disable button
#             button.setText("No more shapes!")
#             button.setDisabled(True)
            
        
# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     frame = MainFrame()
#     frame.show()
    
#     exit_code = app.exec_()
#     sys.exit(exit_code)
#     
#     
#     
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import sys
import numpy
import json
import random
import logging

from DrawPattern import *
from HopfieldMatrixView import *
from HopfieldMatrix import *

SQUARE_WIDTH = 30


class Window(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Réseau de Hopfield")
        self.setWindowState(Qt.WindowMaximized)
        self.show()

        self.NB_COLUMN = 5
        self.NB_ROW = 5

        self.canvasPatterns = QGraphicsView()
        self.scenePatterns = QGraphicsScene(self.canvasPatterns)
        self.canvasPatterns.setScene(self.scenePatterns)

        self.canvasPatterns.mouseMoveEvent = self.mouseMoveEvent
        self.canvasPatterns.mousePressEvent = self.mousePressEvent

        self.currentPattern = []
        self.patterns = []

        spinBoxNBColumn = QSpinBox()
        spinBoxNBColumn.setMaximum (20)
        spinBoxNBColumn.setMinimum (2)
        spinBoxNBColumn.setValue (self.NB_COLUMN)
        spinBoxNBColumn.valueChanged.connect(self.changeNBColumn)

        spinBoxNBRow = QSpinBox()
        spinBoxNBRow.setMaximum (20)
        spinBoxNBRow.setMinimum (2)
        spinBoxNBRow.setValue (self.NB_ROW)
        spinBoxNBRow.valueChanged.connect(self.changeNBRow)

        buttonAddPattern = QPushButton()
        buttonAddPattern.setText("Ajouter pattern")
        buttonAddPattern.clicked.connect(self.addPattern)

        self.hopfieldMatrix = HopfieldMatrix()
        self.hopfieldMatrixView = HopfieldMatrixView(self.hopfieldMatrix,self.NB_COLUMN,SQUARE_WIDTH,self)
        self.hopfieldMatrixView.mousePressEvent = self.mousePressEventHopfiedl

        widget = QWidget(self)
        layout = QGridLayout(widget)
        self.setCentralWidget(widget)

        layout.addWidget(spinBoxNBColumn,1,1)
        layout.addWidget(spinBoxNBRow,1,2)
        layout.addWidget(buttonAddPattern,1,3)

        layout.addWidget(self.canvasPatterns,3,1,1,2)
        layout.addWidget(self.hopfieldMatrixView ,2,1,1,2)


        self.initPattern()
        self.drawData()


    def changeNBColumn(self,newValue):
        self.NB_COLUMN = newValue
        self.update()
        

    def changeNBRow(self,newValue):
        self.NB_ROW = newValue
        self.update()
        

    def drawData(self):
        self.scenePatterns.clear()
        addPatternToScene(self.scenePatterns,self.currentPattern,0,0,self.NB_COLUMN,SQUARE_WIDTH)


    def initPattern(self):
        self.currentPattern = []
        for i in range(self.NB_COLUMN*self.NB_ROW):
            self.currentPattern.append(-1.0)
    
    def update(self):
        self.hopfieldMatrixView.nbCol = NB_COLUMN
        self.initPattern()
        self.drawData()


    def mouseMoveEvent(self,event):
        posMouse = self.canvasPatterns.mapToScene(event.pos())
        
        col = int(posMouse.x()/SQUARE_WIDTH)
        lin = int(posMouse.y()/SQUARE_WIDTH)

        # print(lin,col)
        # print(posMouse.y(),posMouse.x())
        # print(posMouse.y(),posMouse.x())
        # print("_")

        if(col >= 0 and col < self.NB_COLUMN and lin >= 0 and lin < self.NB_ROW):
            if event.buttons() == Qt.LeftButton:
                self.currentPattern[lin*self.NB_COLUMN + col] = 1.0
            elif event.buttons() == Qt.RightButton:
                self.currentPattern[lin*self.NB_COLUMN + col] = -1.0
            
            self.drawData()

    def addPattern(self):
        self.patterns.append(self.currentPattern[:])
        self.hopfieldMatrix.datas = self.patterns
        self.hopfieldMatrixView.datas = []
        for i in range(len(self.hopfieldMatrix.datas)):
            
            self.hopfieldMatrix.datasActived.append(True)

        # self.hopfieldMatrixView.learnFromDatas()
        self.hopfieldMatrixView.drawLearnedPatterns()
        # print(self.hopfieldMatrixView.hopfieldMatrix.datas)
    
    def mousePressEventHopfiedl(self,event):
        posMouse = self.hopfieldMatrixView.mapToScene(event.pos())
        indexPattern = self.hopfieldMatrixView.getIndexOfPattern(posMouse)

        if(indexPattern!=-1):
            self.hopfieldMatrix.datas.pop(indexPattern)
            self.hopfieldMatrixView.drawLearnedPatterns()


app    = QApplication(sys.argv)
window = Window()

sys.exit(app.exec_())