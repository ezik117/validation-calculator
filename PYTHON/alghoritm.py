import msvcrt

class Regisry:
	def __init__(self, name:str, base:'Calc'):
		self.name = name #что бы избежать ссылки на самого себя
		self.value = '0'
		self.base = base
	# сброс содержимого регистра
	def clear(self):
		self.value = '0'
	# затереть один символ с конца
	def BS(self):
		if len(self.value) > 1:
			self.value = self.value[:-1]
		else:
			self.value = '0'
	# ввести один символ в конец
	def input(self, c:str):
		if len(self.value) == 1 and self.value == "0":
			self.value = c
		else:
			self.value += c
	# копировать значения из другого регистра
	def copyFrom(self, R:'Regisry'):
		self.value = R.value
		
class Flags:
	def __init__(self):
		# clear display, 1-означает что новый ввод в A затрет старые результаты
		# , а так же в комбинации с OP=1, что в А есть число
		# , 0-ввод в регистр А разрешен
		self.CD = True
		# constant, 1-означает незавершенную операцию. Незавершенная операция, это последовательный
		# ввод арифметических действий, пока не будет нажата EQ. В случае незавершенной операции
		# вычисления ведуться как B op A. Если операция завершена, то предполагается что второго операнда
		# нет и он берется из регистра В, и соответственно рассчитывается как A op B.
		# Используется для выбора алгоритма АЛУ.
		self.CONST = False
		# equal - нажата ли клавиша "равно". Используется для выбора алгоритма АЛУ.
		self.EQ = False
	def clear(self):
		self.CD = True
		self.CONST = False
		self.EQ = False

class Calc:
	def __init__(self):
		self.A = Regisry('A', self) # регистр A
		self.B = Regisry('B', self) # регистр B
		self.Z = Regisry('Z', self) # симуляция регистра АЛУ
		self.OP = None              # текущее арифметическое действие
		self.flags = Flags()
	# общий сброс
	def clear(self):
		self.A.clear()
		self.B.clear()
		self.Z.clear()
		self.OP = None
		self.flags.clear()
	# отобразить содержимое регистров, 0-все (defaul), 1-только активный регистр
	def displayRegisters(self, mode:int = 0):
		if mode == 0:
			print(f"A='{self.A.value}'  ({self.OP})  B='{self.B.value}'  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}")
		else:
			print("\r" + " "*80, end="")
			print("\r" + self.A.value, end='')
	# ввод значения в регистр A
	def input(self, c):
		if calc.flags.CD:
			self.A.clear()
		if c == '\x08':
			self.A.BS()
		else:
			calc.flags.CD = False
			self.A.input(c)
	# нажата арифметическая клавиша - обработаем
	def pressedOpcode(self, c):
		if not self.flags.CD:
			if self.flags.CONST:
				self.ALU(self.B, self.A)
		self.B.copyFrom(self.A)
		self.OP = c
		self.flags.CD = True
		self.flags.CONST = True

	# нажато равно - обработаем
	def pressedEqual(self):
		if self.flags.CONST:
			self.ALU(self.B, self.A)
		else:
			self.ALU(self.A, self.B)

		self.flags.CD = True
		self.flags.CONST = False


	# функция математики
	def ALU(self, A:Regisry, B:Regisry):
		if self.OP == '+':
			self.Z.value = str(float(A.value) + float(B.value))
		elif self.OP == '-':
			self.Z.value = str(float(A.value) - float(B.value))
		elif self.OP == '/':
			self.Z.value = str(float(A.value) / float(B.value))
		elif self.OP == '*':
			self.Z.value = str(float(A.value) * float(B.value))
		else:
			return # нет операции

		# выбор алгоритма вывода результатов
		if self.flags.EQ and self.flags.CONST:
			self.B.copyFrom(self.A) 
			self.A.copyFrom(self.Z) 
		elif self.flags.EQ and not self.flags.CONST:
			self.A.copyFrom(self.Z)
		elif not self.flags.EQ and self.flags.CONST:
			self.A.copyFrom(self.Z)
			self.B.copyFrom(self.A)
		else:
			raise Exception("ALU: unknown flags combination")


calc = Calc()
print("press 'q' to exit, 0-9 to enter value, 'ESC'-to clear, 'ENTER' to evaluate")
calc.clear()
calc.displayRegisters(mode=0)

while (True):
	if msvcrt.kbhit():
		c = msvcrt.getch().decode()

		# quit
		if c == 'q':
			break

		# digital keys
		if ('0' <= c <= '9') or (c == '\x08'):
			calc.flags.EQ = False
			calc.input(c)
		# reset key
		elif c == '\x1B':
			calc.clear()
		# opcode keys
		elif c in ['+', '-', '*', '/']:
			calc.flags.EQ = False
			calc.pressedOpcode(c)
		# equal key
		elif c == '\x0D':
			calc.flags.EQ = True
			calc.pressedEqual()

		calc.displayRegisters(mode=0)


