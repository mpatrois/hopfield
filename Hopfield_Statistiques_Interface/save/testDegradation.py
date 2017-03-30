from pylab import *

import random

# import pdb; pdb.set_trace()

from HopfieldMatrix     import HopfieldMatrix
from Pattern            import Pattern

NB_NEURONS = 100
NB_TOTAL_PATTERNS = 20
NB_RUNS = 200

transferFunction = {
  'first'  : Pattern.firstFunction,
  'second' : Pattern.secondFunction,
  'third'  : Pattern.thirdFunction
}

noiseFunction = {
  'standard'           : Pattern.makeNoiseStandard,
  'dégradation gauche' : Pattern.makeNoiseLeft,
  'dégradation droite' : Pattern.makeNoiseRight,
  'dégradation centre' : Pattern.makeNoiseCenter
}

def makeARandomPattern(sizePattern):
	return [ random.choice([-1.0,1.0]) for i in range(sizePattern) ]


def makeAStat(nbPatternsToLearn,noisePercentage):
	stat = []

	HopfieldMatrix.NOISE = noisePercentage

	for numberOfPattern in range(1,nbPatternsToLearn):
		hopfieldNtwrk = HopfieldMatrix()
		hopfieldNtwrk.dataToLearn = []

		for i in range(numberOfPattern):
			hopfieldNtwrk.dataToLearn.append(makeARandomPattern(NB_NEURONS))

		hopfieldNtwrk.testPatterns()
		stat.append(hopfieldNtwrk.totalEfficiency())

	return stat

statsForNbPatterns = []

for noise in [30]:
	for typeNoise in noiseFunction:
		Pattern.makeNoise = noiseFunction[typeNoise]
		for cpt in range(NB_RUNS):
			statsForNbPatterns.append(makeAStat(NB_TOTAL_PATTERNS,noise))

		statsNumberPatterns = np.mean( np.array(statsForNbPatterns), axis=0 )
		plot(range(1,NB_TOTAL_PATTERNS), statsNumberPatterns,label='Type de dégradation : ' + typeNoise + ' ('+ str(noise) +"%)")

xlim(1, NB_TOTAL_PATTERNS-1)
xlabel("Nombre de patterns appris")
ylabel("Performance de récuparation")
legend()
show()