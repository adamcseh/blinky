class Color:
	def __init__(self, color:str='', intensity:float=0.0):
		if color.upper()=="HUPIKEK":
			self.green = 10
			self.red = 25
			self.blue = 255
		elif color.upper()=="WHITE":
			self.green = 255
			self.red = 255
			self.blue = 255
		else:
			self.green = 0.0
			self.red = 0.0
			self.blue = 0.0
		self.intensity = intensity
	def getColorCode(self):
		return int(self.intensity/100*self.blue+self.intensity/100*self.red*2**8+self.intensity/100*self.green*2**16)
	
c = Color("hupikek", intensity=100)
print(c.getColorCode())
c = Color("hupikek", intensity=1)
print(c.getColorCode())
