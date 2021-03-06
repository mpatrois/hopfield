from PyQt5.QtCore import *
from PyQt5.QtGui  import *

import sys
import numpy
import json
import random
import logging

from DrawPattern import *
from HopfieldMatrixView import *
from HopfieldMatrix import *

SQUARE_WIDTH = 4

class Window(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Réseau de Hopfield")
        # self.setWindowState(Qt.WindowMaximized)
        self.show()

        self.NB_COLUMN = 5
        self.NB_ROW = 5

        self.canvasPatterns = QGraphicsView()
        self.scenePatterns = QGraphicsScene(self.canvasPatterns)
        self.canvasPatterns.setScene(self.scenePatterns)

        self.canvasPatterns.mouseMoveEvent = self.mouseMoveEvent
        self.canvasPatterns.mousePressEvent = self.mouseMoveEvent

        self.currentPattern = []
        self.patterns = []


        self.nameFileSaved = QLineEdit()
        self.nameFileSaved.setMaximumWidth(200)

        rowLabel = QLabel('Nombre de ligne')
        rowLabel.setMaximumWidth(200)
        colLabel = QLabel('Nombre de colonne')
        colLabel.setMaximumWidth(200)
        fileNameLabel = QLabel('Nom du fichier')
        fileNameLabel.setMaximumWidth(200)
        

        buttonClearPatterns = QPushButton()
        buttonClearPatterns.setText("Clear")
        buttonClearPatterns.clicked.connect(self.clearPattern)
        

        spinBoxNBColumn = QSpinBox()
        spinBoxNBColumn.setMaximum (100)
        spinBoxNBColumn.setMinimum (1)
        spinBoxNBColumn.setValue (self.NB_COLUMN)
        spinBoxNBColumn.valueChanged.connect(self.changeNBColumn)
        spinBoxNBColumn.setMaximumWidth(200)

        spinBoxNBRow = QSpinBox()
        spinBoxNBRow.setMaximum (100)
        spinBoxNBRow.setMinimum (1)
        spinBoxNBRow.setValue (self.NB_ROW)
        spinBoxNBRow.valueChanged.connect(self.changeNBRow)
        spinBoxNBRow.setMaximumWidth(200)

        buttonAddPattern = QPushButton()
        buttonAddPattern.setText("Ajouter le patron courant")
        buttonAddPattern.clicked.connect(self.addPattern)  
        buttonAddPattern.setMaximumWidth(200)

        buttonExportPatterns = QPushButton()
        buttonExportPatterns.setText("Exporter les patterns")
        buttonExportPatterns.clicked.connect(self.exportToFile)

        self.hopfieldMatrix = HopfieldMatrix()
        self.NB_COLUMN = self.hopfieldMatrix.nbCol

        self.hopfieldMatrixView = HopfieldMatrixView(self.hopfieldMatrix,SQUARE_WIDTH,self)
        self.hopfieldMatrixView.canvasLearnedData.mousePressEvent = self.mousePressEventHopfiedl

        widget = QWidget(self)

        layout = QGridLayout(widget)
        self.setCentralWidget(widget)

        
        layout.addWidget(fileNameLabel,1,1)
        layout.addWidget(self.nameFileSaved,2,1)

        layout.addWidget(buttonExportPatterns,2,2)
        
        layout.addWidget(colLabel,3,1)
        layout.addWidget(spinBoxNBColumn,4,1)

        layout.addWidget(buttonClearPatterns,4,4)
        
        layout.addWidget(rowLabel,3,2)
        layout.addWidget(spinBoxNBRow,4,2)
        layout.addWidget(buttonAddPattern,4,3)
        
        layout.addWidget(self.canvasPatterns,5,1,1,6)
        
        layout.addWidget(self.hopfieldMatrixView.canvasLearnedData,6,1,1,6)

        self.update()

    def clearPattern(self,event):
        self.initPattern()
        self.drawData()

    def changeNBColumn(self,newValue):
        self.NB_COLUMN = newValue
        self.update()
        

    def changeNBRow(self,newValue):
        self.NB_ROW = newValue
        self.update()

    def resizeAllCanvas(self):
        self.canvasPatterns.setMinimumHeight(SQUARE_WIDTH * self.NB_ROW + SQUARE_WIDTH)
        self.canvasPatterns.setMaximumHeight(SQUARE_WIDTH * self.NB_ROW + SQUARE_WIDTH) 

        self.hopfieldMatrixView.canvasLearnedData.setMinimumHeight(SQUARE_WIDTH * self.NB_ROW + SQUARE_WIDTH)
        self.hopfieldMatrixView.canvasLearnedData.setMaximumHeight(SQUARE_WIDTH * self.NB_ROW + SQUARE_WIDTH)


    def exportToFile(self,event):
        nameFile = self.nameFileSaved.text()

        dataToExport = {}
        dataToExport['nb_col'] = self.NB_COLUMN
        dataToExport['patterns'] = self.hopfieldMatrix.dataToLearn

        # print (self.hopfieldMatrix.dataToLearn)
        
        with open('patternsCreated/'+nameFile+'.json', 'w') as outfile:
            json.dump(dataToExport, outfile)
        
        

    def drawData(self):
        self.scenePatterns.clear()
        addPatternToScene(self.scenePatterns,self.currentPattern,0,0,self.NB_COLUMN,SQUARE_WIDTH)


    def initPattern(self):
        self.currentPattern = []
        for i in range(self.NB_COLUMN*self.NB_ROW):
            self.currentPattern.append(-1.0)
    
    def update(self):
        self.hopfieldMatrixView.hopfieldMatrix.nbCol = self.NB_COLUMN
        self.hopfieldMatrixView.nbRow = self.NB_ROW
        self.initPattern()
        self.patterns = []
        self.hopfieldMatrix.dataToLearn = self.patterns
        self.drawData()
        self.hopfieldMatrixView.drawLearnedPatterns()

        self.resizeAllCanvas()

    def mouseMoveEvent(self,event):
        posMouse = self.canvasPatterns.mapToScene(event.pos())
        
        col = int(posMouse.x()/SQUARE_WIDTH)
        lin = int(posMouse.y()/SQUARE_WIDTH)

        if(col >= 0 and col < self.NB_COLUMN and lin >= 0 and lin < self.NB_ROW):
            if event.buttons() == Qt.LeftButton:
                self.currentPattern[lin*self.NB_COLUMN + col] = 1.0
            elif event.buttons() == Qt.RightButton:
                self.currentPattern[lin*self.NB_COLUMN + col] = -1.0
            
            self.drawData()

    def addPattern(self):
        self.patterns.append(self.currentPattern[:])
        self.hopfieldMatrix.dataToLearn = self.patterns
        self.hopfieldMatrixView.datas = []
        for i in range(len(self.hopfieldMatrix.dataToLearn)):
            self.hopfieldMatrix.dataToLearnActived.append(True)

        self.hopfieldMatrixView.drawLearnedPatterns()
        
        self.resizeAllCanvas()


    
    def mousePressEventHopfiedl(self,event):
        posMouse = self.hopfieldMatrixView.canvasLearnedData.mapToScene(event.pos())
        indexPattern = self.hopfieldMatrixView.getIndexOfPattern(posMouse)
        if(indexPattern!=-1):
            self.hopfieldMatrix.dataToLearn.pop(indexPattern)
            self.hopfieldMatrixView.drawLearnedPatterns()
            self.resizeAllCanvas()



app    = QApplication(sys.argv)
window = Window()

sys.exit(app.exec_())