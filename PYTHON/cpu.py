from registers import Registry, RegistryZ

# TODO реконструкция ALU
# Причины:
# 1) необходимо реализовать математическую логику для 4 действий (+-/*)
# Реализация:
# - [x] Получить 2 части числа через генератор yield
# - [x] получить длину каждой части, чтобы выравнивать их
# - [x] реализовать логику для сложения
# - [x] реализовать логику для вычитания
# - [x] нужен метод определения большего и меньшего из двух операндов (регистров)
# - [ ] реализовать логику для умножения
# - [ ] реализовать логику для деления

# ------------- АРИФМЕТИЧЕСКО-ЛОГИЧЕСКОЕ УСТРОЙСТВО (АЛУ) ------------ #

class CPU:

	def __init__(self, flags: object):
		self.__flags = flags
		# NEWIT core ref добавляем в АЛУ регистры А и В
		self.__GPRs = {
			'A': Registry('A'),
			'B': Registry('B'),
			'Z': RegistryZ()
		}
		# self.__A = Registry('A')
		# self.__B = Registry('B')
		# self.__Z = RegistryZ()  # виртуальный регистр АЛУ

	# TODO удалить
	@property
	def Z(self):
		return self.__GPRs['Z']
		# return self.__Z

	# NEWIT core ref свойства регистров
	@property
	def B(self):
		return self.__GPRs['B']
		# return self.__B
	
	@property
	def A(self):
		return self.__GPRs['A']
		# return self.__A

	# очистка АЛУ
	def clear(self):
		# NEWIT core ref очистка регистров
		for reg in self.__GPRs:
			reg.clear()
		# self.__A.clear()
		# self.__B.clear()
		# self.__Z.clear()

	# NEWIT core ref делегирование методом input и BS
	def input(self, c):
		self.__GPRs['A'].input(c, self.__flags)
		# self.__A.input(c, self.__flags)

	def BS(self):
		self.__GPRs['A'].BS()
		# self.__A.BS()

	def truncate(self):
		self.__GPRs['A'].truncate()
		# self.__A.truncate()

	# IN: A - ссылка на регистр A
	# IN: B - ссылка на регистр B
	# IN: op - обрабатываемая операция
	# NEWIT core ref обработка теперь в отдельном методе
	def __operate(self, A: Registry, B: Registry, op: str):
		# очистка регистра перед вычислением (лучше бы после, чтобы не хранить значение)
		self.__GPRs['Z'].clear()
		if op == '+':
			self.__GPRs['Z'].value = B.value + A.value
		elif op == '-':
			self.__GPRs['Z'].value = B.value - A.value
		elif op == '/':
			self.__GPRs['Z'].value = str(float(B.value) / float(A.value))
		elif op == '*':
			self.__GPRs['Z'].value = str(float(B.value) * float(A.value))
		# else:
		# 	return  # нет операции

		# TODO возможно, нужно будет очищать незначащие 0 целой части
		# NEWIT удаление незначащих нулей дробной части
		self.__GPRs['Z'].truncate()

		# выбор алгоритма вывода результатов
		# если нажата "равно" и операция не завершена
	# NEWIT core ref алгоритм работы АЛУ
	def process(self, op: str):
		# Когда нажата "равно" флаг CD не имеет значения
		if self.__flags.IS_EQUAL_PRESSED:
			if self.__flags.IS_OPS_CONTINUES:
				self.__operate(self.A, self.B, op)
				if op == '-':
					self.A.value.sign = ~self.A.value.sign
				self.B.copyFrom(self.A)
				self.A.copyFrom(self.Z)
			# если нажата "равно" и операция завершена
			else:
				self.__operate(self.B, self.A, op)
				if op == '-':
					self.B.value.sign = ~self.B.value.sign
				self.A.copyFrom(self.Z)
		# если НЕ нажато "равно" нужно отследить оба флага - CD и CONST
		else:
			if self.__flags.IS_OPERATON_POSSIBLE:
				self.__operate(self.A, self.B, op)
				self.A.copyFrom(self.Z)
			self.B.copyFrom(self.A)
		# NEWIT нет никаких других операций, все охватывает данный выбор
		# ??? очистить регистр Z, чтобы не забивать память
		# self.clear()
