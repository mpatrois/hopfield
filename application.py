#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc.corsini@u-bordeaux2.fr>"
__date__ = "01.10.13"
__usage__ = "Hopfield synchrone"

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

class Window(QMainWindow):

    def __init__(self,patternsView,hopfieldMatrixView):
      QMainWindow.__init__(self)
      self.setWindowTitle("Réseau de Hopfield")
      self.setGeometry(50, 50, 500, 500)
      self.path = QPainterPath()
      self.mainMenu  = self.menuBar()
      
      self.initMenuBar()

      self.patternsView = patternsView
      self.hopfieldMatrixView = hopfieldMatrixView


    def paintEvent(self, event):
      painter = QPainter()
      painter.begin(self)
      painter.setRenderHint(QPainter.Antialiasing)        
      
      painter.setPen(QPen(Qt.black))
      
      for patternIndex, patternView in enumerate(self.patternsView):
       y = patternIndex * ( patternView.getHeight() + 10 )
       patternView.drawSteps(painter,30,y + 100)

      self.hopfieldMatrixView.drawDataLearned(painter,30,10)

      painter.drawPath(self.path)
      painter.end()

    def initMenuBar(self):
      extractAction = QAction("&Nouveau", self)
      extractAction.setShortcut("Ctrl+N")
      extractAction.setStatusTip('Créer un nouveau réseau')

      fileMenu  = self.mainMenu.addMenu('&Reseau')
      fileMenu.addAction(extractAction)

def generateDatasFromFile():
  datas = []
  with open('data/testPatterns.json') as data_file:    
    datas = json.load(data_file)
  return datas  


def generateDatasRamdomly():
  datas = []
  for k in range(10):
      data = []
      for k in range(5*5):
        data.append(random.choice([0,1]))
      datas.append(data)
  return datas  



SQUARE_WIDTH = 10
NB_COLUMN = 5


hopfieldMatrix = HopfieldMatrix()
hopfieldMatrix.loadDataByFile('data/data.json')
hopfieldMatrix.learnFromDatas()

hopfieldMatrixView = HopfieldMatrixView(hopfieldMatrix,NB_COLUMN,SQUARE_WIDTH)


patterns = []
datas    = generateDatasFromFile()

for data in datas:
  pattern = Pattern(data,False)
  pattern.calculAllSteps(hopfieldMatrix.matrix)
  patterns.append(pattern)

patternsView = []
for pattern in patterns:
  patternView = PatternView(pattern,NB_COLUMN,SQUARE_WIDTH)
  patternsView.append(patternView)

app    = QApplication(sys.argv)
window = Window(patternsView,hopfieldMatrixView)
window.show()

sys.exit(app.exec_())