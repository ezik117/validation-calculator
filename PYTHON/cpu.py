from registers import Registry, RegistryZ
import flags

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

	def __init__(self):
		self.__flags = flags.Flags()
		# NEWIT core ref добавляем в АЛУ регистры А и В
		# GPRs - регистры общего назначения (РОН)
		self.__GPRs = {
			'A': Registry('A'),
			'B': Registry('B'),
			'Z': RegistryZ()
		}
		# сохраняет вид операции, чтобы не гонять его по всем функциям
		# DEPRECATED 06-06-2020 используем флаг PI
		# self.__OP = None

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

	# DEPRECATED 06-06-2020 вывод из Flags
	# @property
	# def OP(self):
	# 	return self.__OP

	@property
	def flags(self):
		return self.__flags

	def name(self, name):
		return self.__GPRs[name]

	# очистка АЛУ
	def clear(self):
		# NEWIT core ref очистка регистров
		for reg in self.__GPRs:
			self.__GPRs[reg].clear()
		# очистка флагов
		self.__flags.clear()
		# self.__A.clear()
		# self.__B.clear()
		# self.__Z.clear()

	# NEWIT core ref делегирование методом input и BS
	def input(self, c):
		self.A.input(c, self.__flags)
		# self.__A.input(c, self.__flags)

	def BS(self):
		self.A.BS()
		# self.__A.BS()

	def truncate(self):
		self.A.truncate()
		# self.__A.truncate()

	# IN: A - ссылка на регистр A
	# IN: B - ссылка на регистр B
	# IN: op - обрабатываемая операция
	# NEWIT core ref обработка теперь в отдельном методе
	def __operate(self, A: Registry, B: Registry):
		# очистка регистра перед вычислением (лучше бы после, чтобы не хранить значение)
		self.Z.clear()
		if self.__flags.PI == '+':
			self.Z.value = B.value + A.value
		elif self.__flags.PI == '-':
			self.Z.value = B.value - A.value
		elif self.__flags.PI == '/':
			self.Z.value = str(float(B.value) / float(A.value))
		elif self.__flags.PI == '*':
			self.Z.value = str(float(B.value) * float(A.value))
		# else:
		# 	return  # нет операции

		# TODO возможно, нужно будет очищать незначащие 0 целой части
		# NEWIT удаление незначащих нулей дробной части
		self.Z.truncate()

		# выбор алгоритма вывода результатов
		# если нажата "равно" и операция не завершена
	# NEWIT core ref алгоритм работы АЛУ
	def process(self):
		# DEPRECATED 06-06-2020 используется флаг PI
		# self.__OP = op
		# Когда нажата "равно" флаг CD не имеет значения
		if self.__flags.IS_EQUAL_PRESSED:
			if self.__flags.IS_OPS_CONTINUES:
				self.__operate(self.A, self.B)
				if self.__flags.PI == '-':
					self.A.value.sign = ~self.A.value.sign
				self.B.copyFrom(self.A)
				self.A.copyFrom(self.Z)
			# если нажата "равно" и операция завершена
			else:
				self.__operate(self.B, self.A)
				if self.__flags.PI == '-':
					self.B.value.sign = ~self.B.value.sign
				self.A.copyFrom(self.Z)
		# если НЕ нажато "равно" нужно отследить оба флага - CD и CONST
		else:
			if self.__flags.IS_OPERATION_POSSIBLE:
				self.__operate(self.A, self.B)
				self.A.copyFrom(self.Z)
			self.B.copyFrom(self.A)
		# NEWIT нет никаких других операций, все охватывает данный выбор
		# ??? очистить регистр Z, чтобы не забивать память
		# self.clear()

# -------------------------- Методы для GPRs ------------------------- #

	def get_regnames(self):
		return self.__GPRs.keys()

# --------------------------- Объект знака --------------------------- #

	# class __PI:

	# 	def __init__(self):
	# 		self.__op = None

	# 	@property
	# 	def OP(self):
	# 		return self.__op

	# 	def __call__(self, value):
	# 		if value in set('+-*/'):
	# 			self.__op = value
	# 		else:
	# 			raise TypeError(f"unknown operation: {value}")