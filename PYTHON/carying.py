class Calc:
	X = 0
	Y = 0
	op = None
	IN = None

	def print(self):
		print(f"IN={self.IN},  X={self.X},  Y={self.Y},  op={self.op}")

	def setX(self, x):
		self.X = x
		self.IN = str(x)
		self.print()

	def ALU(self):
		if self.op == '+':
			return self.Y + self.X
		elif self.op == '-':
			return self.Y - self.X
		elif self.op == '*':
			return self.Y * self.X
		elif self.op == '/':
			return self.Y / self.X

	def OP(self, op):
		self.IN = op
		if self.op:
			self.X = self.ALU()
		self.Y = self.X
		self.op = op
		self.print()

c = Calc()
"""
c.setX(5)
c.OP('+')
c.setX(6)
c.OP('-')
c.setX(3)
c.OP('*')
c.setX(2)
c.OP('*')
"""

c.setX(5)
c.OP('+')
c.OP('-')