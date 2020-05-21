from registers import Registry, RegistryZ

# TODO реконструкция ALU
# Причины:
# 1) необходимо реализовать математическую логику для 4 действий (+-/*)
# Реализация:
# - [x] Получить 2 части числа через генератор yield
# - [x] получить длину каждой части, чтобы выравнивать их
# - [x] реализовать логику для сложения
# - [ ] реализовать логику для вычитания
# - [x] нужен метод определения большего и меньшего из двух операндов (регистров)
# - [ ] реализовать логику для умножения
# - [ ] реализовать логику для деления

# ------------- АРИФМЕТИЧЕСКО-ЛОГИЧЕСКОЕ УСТРОЙСТВО (АЛУ) ------------ #

class ALU:

	def __init__(self, flags: object):
		self.__flags = flags
		# NEWIT core ref добавляем в АЛУ регистры А и В
		self.__A = Registry('A')
		self.__B = Registry('B')
		# Регистр Z определяется через свой конструктор
		self.__Z = RegistryZ()  # виртуальный регистр АЛУ

	# TODO удалить
	@property
	def Z(self):
		return self.__Z

	# NEWIT core ref свойства регистров
	@property
	def B(self):
		return self.__B
	
	@property
	def A(self):
		return self.__A

	# очистка АЛУ
	def clear(self):
		# NEWIT core ref очистка регистров
		self.__A.clear()
		self.__B.clear()
		self.__Z.clear()

	# NEWIT core ref делегирование методом input и BS
	def input(self, c):
		# FIXME flag CD
		self.__A.input(c, self.__flags)

	def BS(self):
		self.__A.BS()

	def truncate(self):
		self.__A.truncate()

	# IN: A - ссылка на регистр A
	# IN: B - ссылка на регистр B
	# IN: op - обрабатываемая операция
	# NEWIT core ref обработка теперь в отдельном методе
	def __operate(self, A: Registry, B: Registry, op: str):
		# очистка регистра перед вычислением (лучше бы после, чтобы не хранить значение)
		# NEWIT замена на очистку АЛУ, которая включает очистку регистра Z
		self.__Z.clear()
		# print(A.value)
		# print(A.value < 55)
		if op == '+':
			self.__Z.value = B.value + A.value
		elif op == '-':
			self.__Z.value = B.value - A.value
		elif op == '/':
			self.__Z.value = str(float(B.value) / float(A.value))
		elif op == '*':
			self.__Z.value = str(float(B.value) * float(A.value))
		# else:
		# 	return  # нет операции

		# TODO возможно, нужно будет очищать незначащие 0 целой части
		# NEWIT удаление незначащих нулей дробной части
		self.__Z.truncate()
		# NEWIT если имя внутри метода не соотвествует имени регистра, то нужно менять
		# изначально АЛУ был методом кальулятора, поэтому использовал объекты self
		# if A.name != 'A':
		# 	A, B = B, A
		# выбор алгоритма вывода результатов
		# если нажата "равно" и операция не завершена
		# FIXME после равно и нажатии действия операция проводиться с предыдущим значением
	# NEWIT core ref алгоритм работы АЛУ
	def process(self, op: str):
		# Когда нажата "равно" флаг CD не имеет значения
		if self.__flags.IS_EQUAL_PRESSED:
			if self.__flags.IS_OPS_CONTINUES:
				self.__operate(self.__A, self.__B, op)
				self.__B.copyFrom(self.__A)
				self.__A.copyFrom(self.__Z)
			# если нажата "равно" и операция завершена
			else:
				self.__operate(self.__B, self.__A, op)
				self.__A.copyFrom(self.__Z)
		# если НЕ нажато "равно" нужно отследить оба флага - CD и CONST
		else:
			if self.__flags.IS_OPERATON_POSSIBLE:
				self.__operate(self.__A, self.__B, op)
				self.__A.copyFrom(self.__Z)
			self.__B.copyFrom(self.__A)
		# NEWIT нет никаких других операций, все охватывает данный выбор
		# ??? очистить регистр Z, чтобы не забивать память
		# self.clear()
