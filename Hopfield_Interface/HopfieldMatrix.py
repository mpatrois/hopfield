import numpy
import json

from Pattern import Pattern

class HopfieldMatrix:
	
	def __init__(self):
		self.IS_BINARY = False
		self.NOISE = 0
		self.SYNC = True
		self.typeFunction ='second'
		self.typesFunctions = ['first','second','third']

		self.dataToLearn   = []
		self.dataToLearnActived = []
		
		self.dataToTest = []
		self.patternsTested = []

		self.matrix  = numpy.zeros( (0,0) )
		self.nbCol = 5

	def loadDataByFile(self,fileName):
		with open(fileName) as data_file:
			dataJson = json.load(data_file)
			self.dataToLearn = dataJson['patterns']
			self.nbCol = dataJson['nb_col']

		self.activateAllPatterns()
		

	def activateAllPatterns(self):
		self.dataToLearnActived = []
		for i in range(len(self.dataToLearn)):
			self.dataToLearnActived.append(True)

	def learnFromDatas(self):
		lng         = len(self.dataToLearn[0])
		self.matrix = numpy.zeros( (lng,lng) )

		for idx,vector in enumerate(self.dataToLearn) :
			if(self.dataToLearnActived[idx]):
				v = numpy.array([vector])
				self.matrix += v * v.T # v.T = numpy.transpose(v)
		
		self.matrix /= lng

		for x in range(lng):
			self.matrix[x][x] = 0
			
		
	def nbRow(self):
		if(len(self.dataToLearn) > 0 ):
			return int(len(self.dataToLearn[0])/self.nbCol)
		else:
			return 0

	def testPatterns(self):
		self.patternsTested = []
		self.dataToTest = self.dataToLearn[:]

		
		self.changeTypeCoding(self.dataToLearn,self.IS_BINARY)
		self.changeTypeCoding(self.dataToTest,self.IS_BINARY)

		self.learnFromDatas()

		for data in self.dataToTest:
			pattern = Pattern(data,self,self.IS_BINARY)
			if(self.SYNC):
				pattern.calculAllSteps(self.NOISE,self.typeFunction)
			else:
				pattern.calculAllStepsAsync(self.NOISE,self.typeFunction)
			self.patternsTested.append(pattern)

	def changeTypeCoding(self,datas,isBinary):
		lngVector  = len(datas[0])

		for vector in datas :
			for i in range(lngVector):
				if(isBinary and vector[i] == -1.0):
					vector[i] = 0.0
				elif (isBinary == False and vector[i] == 0.0):
					vector[i] = -1.0

	def totalErrorRecuperationAverage(self):
		totalError = 0
		for pattern in self.patternsTested:
			errorPattern = pattern.errorPercentage(pattern.original) 
			totalError += errorPattern
		return (totalError/len(self.patternsTested))