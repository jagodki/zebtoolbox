class GeorohData:
	
	def __init__(self):
		self.coordinates = dict()
		self.pictures = dict()
		self.lfdm = []
	
	def getCoordinates(self, key):
		return self.coordinates[key]
	
	def setCoordinates(self, key, value):
		self.coordinates = {key : value}
	
	def addLfdm(self, value):
		self.lfdm.append(value)
	
	def getPicture(self, key):
		return self.pictures[key]
	
	def setPicture(self, key, value):
		self.pictures = {key : value}
	
