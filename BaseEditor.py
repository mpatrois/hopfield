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
        self.canvasPatterns.mousePressEvent = self.mouseMoveEvent

        self.currentPattern = []
        self.patterns = []

        rowLabel = QLabel('Nombre de ligne')
        rowLabel.setMaximumWidth(200)
        colLabel = QLabel('Nombre de colonne')
        colLabel.setMaximumWidth(200)
        fileNameLabel = QLabel('Nom du fichier')
        fileNameLabel.setMaximumWidth(200)
        

        self.nameFileSaved = QLineEdit()
        self.nameFileSaved.setMaximumWidth(200)
        

        spinBoxNBColumn = QSpinBox()
        spinBoxNBColumn.setMaximum (20)
        spinBoxNBColumn.setMinimum (2)
        spinBoxNBColumn.setValue (self.NB_COLUMN)
        spinBoxNBColumn.valueChanged.connect(self.changeNBColumn)
        spinBoxNBColumn.setMaximumWidth(200)

        spinBoxNBRow = QSpinBox()
        spinBoxNBRow.setMaximum (20)
        spinBoxNBRow.setMinimum (2)
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
        self.hopfieldMatrixView.mousePressEvent = self.mousePressEventHopfiedl

        widget = QWidget(self)

        layout = QGridLayout(widget)
        self.setCentralWidget(widget)

        
        layout.addWidget(fileNameLabel,1,1)
        layout.addWidget(self.nameFileSaved,2,1)

        layout.addWidget(buttonExportPatterns,2,2)
        

        layout.addWidget(colLabel,3,1)
        layout.addWidget(spinBoxNBColumn,4,1)
        
        layout.addWidget(rowLabel,3,2)
        layout.addWidget(spinBoxNBRow,4,2)
        layout.addWidget(buttonAddPattern,4,3)
        
        layout.addWidget(self.canvasPatterns,5,1,1,4)
        
        layout.addWidget(self.hopfieldMatrixView,6,1,1,4)

        self.update()


    def changeNBColumn(self,newValue):
        self.NB_COLUMN = newValue
        self.update()
        

    def changeNBRow(self,newValue):
        self.NB_ROW = newValue
        self.update()


    def exportToFile(self,event):
        nameFile = self.nameFileSaved.text()

        dataToExport = {}
        dataToExport['nb_col'] = self.NB_COLUMN
        dataToExport['patterns'] = self.hopfieldMatrix.datas

        # print (self.hopfieldMatrix.datas)
        
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
        self.hopfieldMatrixView.nbCol = self.NB_COLUMN
        self.initPattern()
        self.patterns = []
        self.hopfieldMatrix.datas = self.patterns
        self.drawData()
        self.hopfieldMatrixView.drawLearnedPatterns()


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
        self.hopfieldMatrix.datas = self.patterns
        self.hopfieldMatrixView.datas = []
        for i in range(len(self.hopfieldMatrix.datas)):
            self.hopfieldMatrix.datasActived.append(True)

        self.hopfieldMatrixView.drawLearnedPatterns()

    
    def mousePressEventHopfiedl(self,event):
        posMouse = self.hopfieldMatrixView.mapToScene(event.pos())
        indexPattern = self.hopfieldMatrixView.getIndexOfPattern(posMouse)

        if(indexPattern!=-1):
            self.hopfieldMatrix.datas.pop(indexPattern)
            self.hopfieldMatrixView.drawLearnedPatterns()


app    = QApplication(sys.argv)
window = Window()

sys.exit(app.exec_())