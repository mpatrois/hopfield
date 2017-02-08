import numpy
import json

from Pattern import Pattern

class HopfieldMatrix:
	
	def __init__(self):
		self.IS_BINARY = False
		self.NOISE = 0
		self.typeFunction ='first'
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
		
		for i in range(lng):
			self.matrix[i,i] = 0

	def nbRow(self):
		if(len(self.dataToLearn) > 1 ):
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
			pattern.calculAllSteps(self.NOISE,self.typeFunction)
			self.patternsTested.append(pattern)

	def changeTypeCoding(self,datas,isBinary):
		lngVector  = len(datas[0])

		for vector in datas :
			for i in range(lngVector):
				if(isBinary and vector[i] == -1.0):
					vector[i] = 0.0
				elif (isBinary == False and vector[i] == 0.0):
					vector[i] = -1.0