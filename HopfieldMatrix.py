import numpy
import json

class HopfieldMatrix:
	
	def __init__(self):
		self.datas   = []
		self.datasActived = []
		self.matrix  = numpy.zeros( (0,0) )
		self.nbCol = 5

	def loadDataByFile(self,fileName):
		with open(fileName) as data_file:
			dataJson = json.load(data_file)
			self.datas = dataJson['patterns']
			self.nbCol = dataJson['nb_col']

			# self.datas = json.load(data_file)
		
		self.datasActived = []

		for i in range(len(self.datas)):
			self.datasActived.append(True)

	def learnFromDatas(self):
		lng         = len(self.datas[0])
		self.matrix = numpy.zeros( (lng,lng) )

		for idx,vector in enumerate(self.datas) :
			if(self.datasActived[idx]):
				v = numpy.array([vector])
				self.matrix += v * v.T # v.T = numpy.transpose(v)
		
		self.matrix /= lng

	def nbRow(self):
		return int(len(self.datas[0])/self.nbCol)