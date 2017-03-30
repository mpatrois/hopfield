from pylab import *

import random

# import pdb; pdb.set_trace()

from HopfieldMatrix     import HopfieldMatrix
from Pattern            import Pattern

NB_NEURONS = 10
NB_TOTAL_PATTERNS = 20
NB_RUNS = 30

def makeARandomPattern(sizePattern):
	return [ random.choice([-1.0,1.0]) for i in range(sizePattern) ]


def makeAStat(nbPatternsToLearn,noisePercentage):
	stat = []
	for numberOfPattern in range(1,nbPatternsToLearn):
		hopfieldNtwrk = HopfieldMatrix()
		hopfieldNtwrk.dataToLearn = []
		hopfieldNtwrk.NOISE = noisePercentage

		for i in range(numberOfPattern):
			hopfieldNtwrk.dataToLearn.append(makeARandomPattern(NB_NEURONS))

		hopfieldNtwrk.testPatterns()
		stat.append(hopfieldNtwrk.totalEfficiency())

	return stat

statsForNbPatterns = []

for noise in [0,30,50]:
	for cpt in range(NB_RUNS):
		statsForNbPatterns.append(makeAStat(NB_TOTAL_PATTERNS,noise))

	statsNumberPatterns = np.mean( np.array(statsForNbPatterns), axis=0 )
	plot(range(1,NB_TOTAL_PATTERNS), statsNumberPatterns,label='Dégradation :' + str(noise)+"%")

xlim(1, NB_TOTAL_PATTERNS-1)
xlabel("Nombre de patterns appris")
ylabel("Performance de récuparation")
legend()
show()