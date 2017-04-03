import numpy
import json
import random

from Pattern import Pattern

class HopfieldMatrix:
	
	def __init__(self,fasPercentage):
		self.FASPERCENTAGE = fasPercentage


		self.dataToLearn   = []
		
		self.dataToTest = []
		self.patternsTested = []

		self.matrix  = numpy.zeros( (0,0) )
		self.matrixFAS  = numpy.zeros( (0,0) )

		self.nbCol = 5

	def loadDataByFile(self,fileName):
		with open(fileName) as data_file:
			dataJson = json.load(data_file)
			self.dataToLearn = dataJson['patterns']
			self.nbCol = dataJson['nb_col']


	def learnFromDatas(self):
		lng         = len(self.dataToLearn[0])
		self.matrix = numpy.zeros( (lng,lng) )

		for idx,vector in enumerate(self.dataToLearn) :
				v = numpy.array([vector])
				self.matrix += v * v.T # v.T = numpy.transpose(v)
		
		self.matrix /= lng

		
		for x in range(lng):
			self.matrix[x][x] = 0

		self.makeFAS(lng,self.FASPERCENTAGE)
		

	
	def makeFAS(self,sizePattern,fasPercentage):

		self.matrixFAS  = numpy.zeros( (sizePattern,sizePattern) )

		nbFasToMake = fasPercentage * (sizePattern) / 100

		for i in range(sizePattern):
			for j in random.sample(range(sizePattern), int(nbFasToMake)):
				typeFas =  numpy.random.random_integers(1,3)
				self.matrixFAS[i][j] = typeFas


	# def makeFASONE(self,sizePattern,fasPercentage):

	# 	self.matrixFAS  = numpy.zeros( (sizePattern,sizePattern) )

	# 	nbFasToMake = fasPercentage * (sizePattern*sizePattern) / 100

	# 	randomI = numpy.random.randint(sizePattern,size=nbFasToMake)
	# 	randomJ = numpy.random.randint(sizePattern,size=nbFasToMake)

	# 	for n in range(len(randomI)):
	# 		typeFas =  numpy.random.random_integers(1,3)
	# 		i = randomI[n]
	# 		j = randomJ[n]


	# 		self.matrixFAS[i,j] = typeFas
		
	def nbRow(self):
		if(len(self.dataToLearn) > 0 ):
			return int(len(self.dataToLearn[0])/self.nbCol)
		else:
			return 0

	def testPatterns(self):
		self.patternsTested = []
		self.dataToTest = self.dataToLearn[:]

		self.learnFromDatas()

		for data in self.dataToTest:
			pattern = Pattern(data,self)
			pattern.calculAllSteps()
			self.patternsTested.append(pattern)


	def totalEfficiency(self):
		totalEfficiency = 0
		for pattern in self.patternsTested:
			totalEfficiency += pattern.recallEfficiency() 
		return (totalEfficiency/len(self.patternsTested))