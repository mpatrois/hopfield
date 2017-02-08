#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import sys
import numpy
import json
import random
import os

from HopfieldMatrix     import HopfieldMatrix
from HopfieldMatrixView import HopfieldMatrixView
from Pattern            import Pattern
from PatternView        import PatternView

SQUARE_WIDTH = 10

class Window(QMainWindow):

    def __init__(self):
      QMainWindow.__init__(self)
      self.show()
     
      self.setWindowTitle("Réseau de Hopfield")
      self.setWindowState(Qt.WindowMaximized)

      self.patterns = []

      self.files = sorted(os.listdir("patternsCreated"))
      self.fileName = 'patternsCreated/' + self.files[0]
      
      self.hopfieldMatrix = HopfieldMatrix()
      self.hopfieldMatrix.loadDataByFile(self.fileName)

      self.hopfieldMatrixView = HopfieldMatrixView(self.hopfieldMatrix,SQUARE_WIDTH,self)

      self.canvasPatterns = QGraphicsView()
      
     
      self.scenePatterns = QGraphicsScene(self.canvasPatterns)
      self.canvasPatterns.setScene(self.scenePatterns)


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


      typeCodeLabel = QLabel('Codage bivalué')
      

      self.binaryComboBox = QComboBox()
      self.binaryComboBox.addItems(["Bipolaire","Binaire"])
      self.binaryComboBox.currentIndexChanged.connect(self.binaryComboBoxChanged)
      


      typeFunctionLabel = QLabel('Fonction de transfert')
      self.typesFunctionComboBox = QComboBox()
      self.typesFunctionComboBox.addItems(self.hopfieldMatrix.typesFunctions)
      self.typesFunctionComboBox.currentIndexChanged.connect(self.typesFunctionComboBoxChanged)

      filesLabel = QLabel('Fichiers')
      self.filesComboBox = QComboBox()
      self.filesComboBox.addItems(self.files)
      self.filesComboBox.currentIndexChanged.connect(self.filesComboBoxChanged)

      layout.addWidget(typeCodeLabel,1,1)
      layout.addWidget(self.binaryComboBox,1,2) 

      layout.addWidget(typeFunctionLabel,2,1)
      layout.addWidget(self.typesFunctionComboBox,2,2)  

      layout.addWidget(filesLabel,2,3)
      layout.addWidget(self.filesComboBox,2,4)
      
      layout.addWidget(noiseLabel,1,3)
      layout.addWidget(spinBoxNoise,1,4)
      
      layout.addWidget(hopfieldLabel,3,1)
      layout.addWidget(self.hopfieldMatrixView,3,2,1,10)
      
      
      layout.addWidget(patternsLabel,4,1,1,2)
      layout.addWidget(self.canvasPatterns,4,2,1,10)
      
      
      self.update()

      

    def drawDatas(self):
      self.hopfieldMatrixView.drawLearnedPatterns()
      self.canvasPatterns.viewport().update()
      self.hopfieldMatrixView.drawTestedPatterns(self.scenePatterns)


    def changeNoise(self,newNoise):
      self.hopfieldMatrix.NOISE = newNoise
      self.update()

    def binaryComboBoxChanged(self,idx):
      value = self.binaryComboBox.itemText(idx)
      
      if( value == "Binaire" ):
        self.hopfieldMatrix.IS_BINARY = True
      elif (value == 'Bipolaire'):
        self.hopfieldMatrix.IS_BINARY = False

      self.update()

    def typesFunctionComboBoxChanged(self,idx):
      value = self.typesFunctionComboBox.itemText(idx)
      self.hopfieldMatrix.typeFunction = value
      self.update()  

    def filesComboBoxChanged(self,idx):
      value = self.filesComboBox.itemText(idx)
      self.fileName = 'patternsCreated/' + value
      self.hopfieldMatrix.loadDataByFile(self.fileName)
      self.update()

    def update(self):
      self.hopfieldMatrix.testPatterns()
      self.drawDatas()


app    = QApplication(sys.argv)
window = Window()

sys.exit(app.exec_())