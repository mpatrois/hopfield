from pylab import *

import random

# import pdb; pdb.set_trace()

from HopfieldMatrix     import HopfieldMatrix
from Pattern            import Pattern

NB_NEURONS = 100
NB_TOTAL_PATTERNS = 10
NB_RUNS = 400
NOISE = 0

def makeARandomPattern(sizePattern):
	newPattern = []
	for i in range(sizePattern):
		neuronValue = random.choice( [-1.0,1.0 ])
		newPattern.append(neuronValue)
	return newPattern


def makeAStat(nbPatternsToLearn,noisePercentage):
	stat = []
	for numberOfPattern in range(1,nbPatternsToLearn):
		hopfieldNtwrk = HopfieldMatrix()
		hopfieldNtwrk.dataToLearn = []
		hopfieldNtwrk.dataToLearnActived = []
		hopfieldNtwrk.noisePercentage = noisePercentage

		for i in range(numberOfPattern):
			hopfieldNtwrk.dataToLearn.append(makeARandomPattern(NB_NEURONS))
			hopfieldNtwrk.dataToLearnActived.append(True)
		hopfieldNtwrk.testPatterns()
		stat.append(hopfieldNtwrk.totalErrorRecuperationAverage())

	
	return stat

statsForNbPatterns = []

for i in range(0,6):
	noise = i * 10
	print(noise)
	for cpt in range(NB_RUNS):
		statsForNbPatterns.append(makeAStat(NB_TOTAL_PATTERNS,noise))

	statsNumberPatterns = np.mean( np.array(statsForNbPatterns), axis=0 )
	plot(range(1,NB_TOTAL_PATTERNS), statsNumberPatterns,label='Noise' + str(noise))

show()