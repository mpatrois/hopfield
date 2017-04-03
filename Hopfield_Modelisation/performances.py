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




def makeARandomPattern(sizePattern,isBinary):
    return [ random.choice([-1.0,1.0]) for i in range(sizePattern) ]


class CanvasStats(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        super(FigureCanvas, self).__init__(fig)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.axes.set_xlabel("Pourcentage de FAS dans le réseau")
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
        self.statsCanvas.axes.set_xlim(0, 100)
        self.statsCanvas.axes.set_ylim(0,1.05)


        nbIterationLabel = QLabel('Nombre de tours')
        spinBoxNbIteration = QSpinBox()
        spinBoxNbIteration.setMaximum (100)
        spinBoxNbIteration.setMinimum (self.NB_RUNS)
        spinBoxNbIteration.valueChanged.connect(self.changeNbIterations)

      

        self.button = QPushButton('Start', self)
        self.button.setToolTip('Lancer les statistiques')
        self.button.clicked.connect(self.startStats)

        layout.addWidget(nbIterationLabel,1,3)
        layout.addWidget(spinBoxNbIteration,1,4)

        layout.addWidget(self.button,4,1,1,4)

        layout.addWidget(self.statsCanvas,5,1,1,4)

        self.setCentralWidget(self.main_widget)

    def changeNbIterations(self,newNbIterations):
        self.NB_RUNS = newNbIterations

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

        self.statsCanvas.axes.set_xlim(0, 100)
        self.statsCanvas.axes.set_ylim(0,1.05)
        self.statsCanvas.axes.set_xlabel("Pourcentage de FAS dans le réseau")
        self.statsCanvas.axes.set_ylabel("Performance de récuparation")

        hopfieldNtwrk = HopfieldMatrix(0)
        hopfieldNtwrk.loadDataByFile('patternsCreated/quatresChiffres.json')
            
        totalStats = []

        for cpt in range(self.NB_RUNS):
            statsForFasPercentage = []
            for fasPercentage in [0,10,20,30,40,50,60,70,80,90,100]:
                hopfieldNtwrk.FASPERCENTAGE = fasPercentage
                hopfieldNtwrk.learnFromDatas()
                hopfieldNtwrk.testPatterns()
                statsForFasPercentage.append(hopfieldNtwrk.totalEfficiency())
            totalStats.append(statsForFasPercentage)
        
        
        total = np.mean( np.array(totalStats), axis=0 )

        self.statsCanvas.axes.plot([0,10,20,30,40,50,60,70,80,90,100], total)
            

        self.statsCanvas.axes.legend()
        self.statsCanvas.draw()
        self.button.setEnabled(True)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.show()

    app.exec_()