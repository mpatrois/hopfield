from pylab import *


import sys
import numpy
import json
import random
import os

from HopfieldMatrix     import HopfieldMatrix
from HopfieldMatrixView import HopfieldMatrixView
from Pattern            import Pattern
from PatternView        import PatternView


NB_NEURONS = 10

listOfHopfieldNetworks = []

def makeARandomPattern(sizePattern):
	newPattern = []
	for i in range(sizePattern):
		neuronValue = random.choice( [-1.0,1.0 ])
		newPattern.append(neuronValue)
	return newPattern


def makeAStat():
	stat = []
	for numberOfPattern in range(1,50):
		hopfieldNtwrk = HopfieldMatrix()
		hopfieldNtwrk.dataToLearn = []
		hopfieldNtwrk.dataToLearnActived = []
		hopfieldNtwrk.noisePercentage = 20

		for i in range(numberOfPattern):
			hopfieldNtwrk.dataToLearn.append(makeARandomPattern(NB_NEURONS))
		
		hopfieldNtwrk.activateAllPatterns()
		hopfieldNtwrk.testPatterns()
		
		listOfHopfieldNetworks.append(hopfieldNtwrk)
		

		stat.append(hopfieldNtwrk.totalErrorRecuperationAverage())
	return stat

nbTest = 1
stats = []
for cpt in range(nbTest):
	stats.append(makeAStat())

finalStat = []
for i in range(1,50):
	finalStat.append(0)

for stat in stats:
	for nbPattern,error in enumerate(stat):
		finalStat[nbPattern] += error 

for i in range(len(finalStat)):
	finalStat[i]= finalStat[i]/nbTest


plot(range(len(finalStat)), finalStat)

show()