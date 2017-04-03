import numpy
import json

from Pattern import Pattern

class HopfieldMatrix:
	
	def __init__(self,isHealthy):
		self.NOISE = 0


		self.dataToLearn   = []
		
		self.dataToTest = []
		self.patternsTested = []

		self.matrix  = numpy.zeros( (0,0) )
		self.matrixFAS  = numpy.zeros( (0,0) )

		self.isHealthy = isHealthy


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

		self.makeFAS(lng)
		print(self.matrixFAS)

	
	def makeFAS(self,size):

		self.matrixFAS  = numpy.zeros( (size,size) )

		for i in range(size):
			for j in range(size):

				if(self.isHealthy == False):

					if(numpy.random.random_integers(3)==1):
						self.matrixFAS[i,j] = 1
					elif(numpy.random.random_integers(3)==1):
						self.matrixFAS[i,j] = 2
					elif(numpy.random.random_integers(3)==1):
						self.matrixFAS[i,j] = 3


	
	def isCorrect(self,step):
		for pattern in self.dataToLearn:
				if( numpy.all( numpy.sign(pattern) == numpy.sign(step) )):
					return True
		return False

			
		
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
			pattern.calculAllSteps(self.NOISE)
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