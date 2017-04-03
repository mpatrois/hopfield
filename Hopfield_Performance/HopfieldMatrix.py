import numpy
import json

from Pattern import Pattern

class HopfieldMatrix:
	
	def __init__(self,isBinary,noise):
		self.IS_BINARY = False
		self.NOISE = noise

		self.dataToLearn   = []
		
		self.patternsTested = []

	def learnFromDatas(self):
		lng         = len(self.dataToLearn[0])
		self.matrix = numpy.zeros( (lng,lng) )

		for vector in self.dataToLearn :
			v = numpy.array([vector])
			self.matrix += v * v.T # v.T = numpy.transpose(v)
		
		self.matrix /= lng

		for x in range(lng):
			self.matrix[x][x] = 0

	def testPatterns(self):
		self.patternsTested = []
		self.learnFromDatas()

		for data in self.dataToLearn:
			pattern = Pattern(data,self,self.IS_BINARY)
			pattern.calculAllSteps(self.NOISE)
			self.patternsTested.append(pattern)

	def totalEfficiency(self):
		totalEfficiency = 0
		for pattern in self.patternsTested:
			totalEfficiency += pattern.recallEfficiency() 
		return (totalEfficiency/len(self.patternsTested))