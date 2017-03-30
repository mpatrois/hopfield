import sys
import random
import matplotlib;matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout,QGridLayout, QSizePolicy, QMessageBox, QWidget, QLabel, QSpinBox, QComboBox, QPushButton
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from HopfieldMatrix     import HopfieldMatrix
from Pattern            import Pattern
from pylab import *
from threading import Thread

import random


transferFunction = {
  'first'  : Pattern.firstFunction,
  'second' : Pattern.secondFunction,
  'third'  : Pattern.thirdFunction
}

synchronicity = {
  'Oui'  : Pattern.calculAllStepsSync,
  'Non'  : Pattern.calculAllStepsAsync,
}

def makeARandomPattern(sizePattern,isBinary):
    if (isBinary):
        return [ random.choice([0.0,1.0]) for i in range(sizePattern) ]
    else:
        return [ random.choice([-1.0,1.0]) for i in range(sizePattern) ]

def makeAStat(nbPatternsToLearn,noisePercentage,nbNeurons,isBinary):
    stat = []
    for numberOfPattern in range(1,nbPatternsToLearn+1):
        hopfieldNtwrk = HopfieldMatrix(isBinary,noisePercentage)
        hopfieldNtwrk.dataToLearn = []
        # hopfieldNtwrk.NOISE = noisePercentage
        # hopfieldNtwrk.IS_BINARY = isBinary

        for i in range(numberOfPattern):
            hopfieldNtwrk.dataToLearn.append(makeARandomPattern(nbNeurons,isBinary))

        hopfieldNtwrk.testPatterns()
        stat.append(hopfieldNtwrk.totalEfficiency())

    return stat

statsForNbPatterns = []



class CanvasStats(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        super(FigureCanvas, self).__init__(fig)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.axes.set_xlabel("Nombre de patterns appris")
        self.axes.set_ylabel("Performance de récuparation")
   

class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Statistiques Hopfield")

        self.NB_NEURONS = 10
        self.NB_TOTAL_PATTERNS = 10
        self.NB_RUNS = 1
        self.IS_BINARY = False


        self.main_widget = QWidget(self)

        layout = QGridLayout(self.main_widget)
        self.statsCanvas = CanvasStats(self.main_widget, width=5, height=4, dpi=100)
        self.statsCanvas.axes.set_xlim(1, self.NB_TOTAL_PATTERNS)
        self.statsCanvas.axes.set_ylim(0,1.05)


        nbIterationLabel = QLabel('Nombre de tours')
        spinBoxNbIteration = QSpinBox()
        spinBoxNbIteration.setMaximum (1000)
        spinBoxNbIteration.setMinimum (self.NB_RUNS)
        spinBoxNbIteration.valueChanged.connect(self.changeNbIterations)


        nbPatternLabel = QLabel('Nombre de motifs par réseaux')
        spinBoxNbPattern = QSpinBox()
        spinBoxNbPattern.setMaximum (50)
        spinBoxNbPattern.setMinimum (self.NB_TOTAL_PATTERNS)
        spinBoxNbPattern.valueChanged.connect(self.changeNbPatterns)
   
        nbNeuronsLabel = QLabel('Nombre de neurones par réseaux')
        spinBoxNbNeurons = QSpinBox()
        spinBoxNbNeurons.setMaximum (1000)
        spinBoxNbNeurons.setMinimum (self.NB_NEURONS)
        spinBoxNbNeurons.valueChanged.connect(self.changeNbNeurons)
      
        typeSynchroneLabel = QLabel('Synchrone')
        self.asyncComboBox = QComboBox()
        self.asyncComboBox.addItems(['Oui','Non'])
        self.asyncComboBox.currentIndexChanged.connect(self.changeSyncronicity)

        typeCodeLabel = QLabel('Codage bivalué')
        self.binaryComboBox = QComboBox()
        self.binaryComboBox.addItems(["Bipolaire","Binaire"])
        self.binaryComboBox.currentIndexChanged.connect(self.changeBinary)

        typeFunctionLabel = QLabel('Fonction de transfert')
        self.typesFunctionComboBox = QComboBox()
        self.typesFunctionComboBox.addItems(['first','second','third'])
        self.typesFunctionComboBox.currentIndexChanged.connect(self.changeTypeFunction)


        self.button = QPushButton('Start', self)
        self.button.setToolTip('Lancer les statistiques')
        self.button.clicked.connect(self.startStats)

        layout.addWidget(typeCodeLabel,1,1)
        layout.addWidget(self.binaryComboBox,1,2) 

        layout.addWidget(typeFunctionLabel,2,1)
        layout.addWidget(self.typesFunctionComboBox,2,2)  

        layout.addWidget(typeSynchroneLabel,3,1)
        layout.addWidget(self.asyncComboBox,3,2)

        layout.addWidget(nbIterationLabel,1,3)
        layout.addWidget(spinBoxNbIteration,1,4)
        
        layout.addWidget(nbPatternLabel,2,3)
        layout.addWidget(spinBoxNbPattern,2,4)
        
        layout.addWidget(nbNeuronsLabel,3,3)
        layout.addWidget(spinBoxNbNeurons,3,4)

        layout.addWidget(self.button,4,1,1,4)

        layout.addWidget(self.statsCanvas,5,1,1,4)

        self.setCentralWidget(self.main_widget)

    def changeNbPatterns(self,newNbPatterns):
        self.NB_TOTAL_PATTERNS = newNbPatterns
        self.statsCanvas.axes.set_xlim(1, self.NB_TOTAL_PATTERNS)
        self.statsCanvas.axes.set_ylim(0,1.05)
        self.statsCanvas.axes.clear()
        self.statsCanvas.draw()

    def changeNbNeurons(self,newNbNeurons):
        self.NB_NEURONS = newNbNeurons

    def changeNbIterations(self,newNbIterations):
        self.NB_RUNS = newNbIterations

    def changeBinary(self,idx):
        value = self.binaryComboBox.itemText(idx)

        if(value == 'Binaire'):
            self.IS_BINARY = True
        else:
            self.IS_BINARY = False

    def changeTypeFunction(self,idx):
        value = self.typesFunctionComboBox.itemText(idx)
        Pattern.transferFunction = transferFunction[value]

    def changeSyncronicity(self,idx):
        value = self.asyncComboBox.itemText(idx)
        Pattern.calculAllSteps = synchronicity[value]

    def startStats(self):
        self.button.setEnabled(False)
        self.statsCanvas.axes.clear()
        self.statsCanvas.draw()

        self.statsCanvas.axes.set_xlim(1, self.NB_TOTAL_PATTERNS)
        self.statsCanvas.axes.set_ylim(0,1.05)
        statsForNbPatterns = []


        for noise in [0,10,20,30,40,50]:

            for cpt in range(self.NB_RUNS):
                statsForNbPatterns.append(makeAStat(self.NB_TOTAL_PATTERNS,noise,self.NB_NEURONS,self.IS_BINARY))

            statsNumberPatterns = np.mean( np.array(statsForNbPatterns), axis=0 )
            self.statsCanvas.axes.plot(range(1,self.NB_TOTAL_PATTERNS+1), statsNumberPatterns,label='Dégradation :' + str(noise)+"%")
            

        self.statsCanvas.axes.legend()
        self.statsCanvas.draw()
        self.button.setEnabled(True)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    aw = ApplicationWindow()
    # aw.setWindowTitle("PyQt5 Matplot Example")
    aw.show()

    app.exec_()