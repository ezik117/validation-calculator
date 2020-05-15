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
		# Регистр Z определяется через свой конструктор
		self.__Z = RegistryZ()  # виртуальный регистр АЛУ

	# TODO удалить
	@property
	def Z(self):
		return self.__Z

	# очистка АЛУ
	def clear(self):
		self.__Z.clear()

	# IN: A - ссылка на регистр A
	# IN: B - ссылка на регистр B
	# IN: op - обрабатываемая операция
	def process(self, A: Registry, B: Registry, op: str):
		# очистка регистра перед вычислением (лучше бы после, чтобы не хранить значение)
		# NEWIT замена на очистку АЛУ, которая включает очистку регистра Z
		self.clear()
		print(A.value)
		print(A.value < 55)
		if op == '+':
			self.__Z.value = A.value + B.value
		elif op == '-':
			self.__Z.value = A.value - B.value
		elif op == '/':
			self.__Z.value = str(float(A.value) / float(B.value))
		elif op == '*':
			self.__Z.value = str(float(A.value) * float(B.value))
		else:
			return  # нет операции
		# TODO возможно, нужно будет очищать незначащие 0 целой части
		# NEWIT удаление незначащих нулей дробной части
		self.__Z.truncate()
		# выбор алгоритма вывода результатов
		# если нажата "равно" и операция не завершена
		# FIXME после равно и нажатии действия операция проводиться с предыдущим значением
		if self.__flags.IS_B_op_A:
			# копируем из А в В
			B.copyFrom(A)
			# копируем из Z в А
			A.copyFrom(self.__Z)
		# если нажата "равно" и операция завершена
		elif self.__flags.IS_A_op_B:
			# копируем из Z в А
			A.copyFrom(self.__Z)
		# если НЕ "равно" и операция не завершена
		elif self.__flags.IS_NEXT_OPERATION:
			# копируем из Z в А
			A.copyFrom(self.__Z)
			# копируем из А в В
			B.copyFrom(A)
		# в любом другом случае (нажато НЕ "равно" и операция завершилась)
		else:
			raise Exception("ALU: unknown flags combination")

# ---------------------------- Мои методы ---------------------------- #
