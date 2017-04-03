#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets  import *

import sys
import numpy
import json
import random
import os

from HopfieldMatrix     import HopfieldMatrix
from HopfieldMatrixView import HopfieldMatrixView
from Pattern            import Pattern
from PatternView        import PatternView

SQUARE_WIDTH = 4

class Window(QMainWindow):

    def __init__(self):
      QMainWindow.__init__(self)
      self.show()

      self.HEALTHY = False
     
      self.setWindowTitle("Réseau de Hopfield")
      self.setWindowState(Qt.WindowMaximized)

      self.patterns = []

      self.files = sorted(os.listdir("patternsCreated"))
      self.fileName = 'patternsCreated/' + self.files[0]
      
      self.hopfieldMatrix = HopfieldMatrix( self.HEALTHY)
      self.hopfieldMatrix.loadDataByFile(self.fileName)

      hopfieldLabel = QLabel('Patrons appris :')
      patternsLabel = QLabel('Patrons testés :')
      self.hopfieldMatrixView = HopfieldMatrixView(self.hopfieldMatrix,SQUARE_WIDTH,self)

      widget = QWidget(self)
      layout = QGridLayout(widget)
      self.setCentralWidget(widget)

      noiseLabel = QLabel('Taux de bruitage (%)')
      spinBoxNoise = QSpinBox()
      spinBoxNoise.setMaximum (100)
      spinBoxNoise.setMinimum (0)
      spinBoxNoise.valueChanged.connect(self.changeNoise)


      filesLabel = QLabel('Fichiers')
      self.filesComboBox = QComboBox()
      self.filesComboBox.addItems(self.files)
      self.filesComboBox.currentIndexChanged.connect(self.filesComboBoxChanged)
  

      layout.addWidget(filesLabel,2,1)
      layout.addWidget(self.filesComboBox,2,2)
      
      layout.addWidget(noiseLabel,1,1)
      layout.addWidget(spinBoxNoise,1,2)
      
      layout.addWidget(hopfieldLabel,3,1)
      layout.addWidget(self.hopfieldMatrixView.canvasLearnedData,3,2,1,10)
      
      layout.addWidget(patternsLabel,4,1,1,2)
      layout.addWidget(self.hopfieldMatrixView.canvasTestedData,4,2,1,10)
      
      self.update()

    def drawDatas(self):
      self.hopfieldMatrixView.drawLearnedPatterns()
      self.hopfieldMatrixView.drawTestedPatterns()

    def changeNoise(self,newNoise):
      self.hopfieldMatrix.NOISE = newNoise
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