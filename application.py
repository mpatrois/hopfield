#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import sys
import numpy
import json
import random

from HopfieldMatrix     import HopfieldMatrix
from HopfieldMatrixView import HopfieldMatrixView
from Pattern            import Pattern
from PatternView        import PatternView

SQUARE_WIDTH = 13
NB_COLUMN = 5


class Window(QMainWindow):

    def __init__(self):
      QMainWindow.__init__(self)
      self.setWindowTitle("Réseau de Hopfield")
      self.setWindowState(Qt.WindowMaximized)
      self.setWindowState(Qt.WindowMaximized)
      self.setWindowState(Qt.WindowMaximized)

      self.NOISE = 0
      self.IS_BINARY = False

      self.patterns = []
      self.patternsView = []
      
      self.hopfieldMatrix = HopfieldMatrix()
      self.hopfieldMatrix.loadDataByFile('data/data.json')

      self.hopfieldMatrixView = HopfieldMatrixView(self.hopfieldMatrix,NB_COLUMN,SQUARE_WIDTH,self)

      canvasPatterns = QGraphicsView()
      self.hopfieldMatrixView.setMaximumHeight(SQUARE_WIDTH * NB_COLUMN + 2)
      self.hopfieldMatrixView.setMinimumHeight(SQUARE_WIDTH * NB_COLUMN + 2)
     
      self.scenePatterns = QGraphicsScene(canvasPatterns)
      canvasPatterns.setScene(self.scenePatterns)


      widget = QWidget(self)
      layout = QGridLayout(widget)
      self.setCentralWidget(widget)


      noiseLabel = QLabel('Taux de bruitage (%)')
      hopfieldLabel = QLabel('Patrons appris :')
      patternsLabel = QLabel('Patrons testés :')
      
      
      spinBoxNoise = QSpinBox()
      spinBoxNoise.setMaximum (100)
      spinBoxNoise.setMinimum (0)
      spinBoxNoise.valueChanged.connect(self.changeNoise)

      self.labelTest = QLabel('Test')

      typeCode = QLabel('Codage bivalué')
      self.binaryComboBox = QComboBox()

      self.binaryComboBox.addItems(["Bipolaire","Binaire"])
      self.binaryComboBox.currentIndexChanged.connect(self.binaryComboBoxChanged)

      layout.addWidget(self.labelTest,1,1)
      layout.addWidget(self.binaryComboBox,1,2)
      

      layout.addWidget(noiseLabel,2,1)
      layout.addWidget(spinBoxNoise,2,2)
      
      layout.addWidget(hopfieldLabel,3,1)
      layout.addWidget(self.hopfieldMatrixView,3,2)
      
      
      layout.addWidget(patternsLabel,4,1)
      layout.addWidget(canvasPatterns,4,2)
      

      self.loadPatternsAndTest()
      self.drawDatas()

      self.show()

    def drawDatas(self):
      self.scenePatterns.clear()
      self.hopfieldMatrixView.drawLearnedPatterns()
      # self.sceneHopfieldMatrix.clear()

      # self.hopfieldMatrixView.addDataLearnedToScene(self.sceneHopfieldMatrix)
      
      for patternIndex, patternView in enumerate(self.patternsView):
       y = patternIndex * ( patternView.getHeight() + SQUARE_WIDTH )
       patternView.addStepsToScene(self.scenePatterns,30,y + SQUARE_WIDTH * NB_COLUMN +2*SQUARE_WIDTH)


    def generateDatasFromFile(self):
      datas = []
      with open('data/testPatterns.json') as data_file:    
        datas = json.load(data_file)
      return datas  

    def generateDatasRamdomly(self):
      datas = []
      for k in range(10):
          data = []
          for k in range(5*5):
            data.append(random.choice([0,1]))
          datas.append(data)
      return datas  

    def loadPatternsAndTest(self):
      
      self.patterns = []
      datas = self.generateDatasFromFile()

      self.changeTypeCoding(datas,self.IS_BINARY)
      self.changeTypeCoding(self.hopfieldMatrix.datas,self.IS_BINARY)
      
      self.hopfieldMatrix.learnFromDatas()

      for data in datas:
        pattern = Pattern(data,self.hopfieldMatrix,self.IS_BINARY)
        pattern.calculAllSteps(self.NOISE)
        self.patterns.append(pattern)

      self.patternsView = []
      for pattern in self.patterns:
        patternView = PatternView(pattern,NB_COLUMN,SQUARE_WIDTH)
        self.patternsView.append(patternView)

    def changeNoise(self,newNoise):
      self.NOISE = newNoise
      self.loadPatternsAndTest()
      self.drawDatas()

    def binaryComboBoxChanged(self,idx):
      value = self.binaryComboBox.itemText(idx)
      
      if( value == "Binaire" ):
        self.IS_BINARY = True
      elif (value == 'Bipolaire'):
        self.IS_BINARY = False

      self.update()

    def changeTypeCoding(self,datas,isBinary):
      lngVector  = len(datas[0])

      for vector in datas :
        for i in range(lngVector):
          if(isBinary and vector[i] == -1.0):
            vector[i] = 0.0
          elif (isBinary == False and vector[i] == 0.0):
            vector[i] = -1.0

    def update(self):
      self.loadPatternsAndTest()
      self.drawDatas()


app    = QApplication(sys.argv)
window = Window()

sys.exit(app.exec_())