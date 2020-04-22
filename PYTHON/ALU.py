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
		# NEWIT хранение ссылок на больший и меньший регистр
		# self.__bigger = None
		# self.__smaller = None
		# NEWIT если оба операнда равны по модулю - True
		# self.__equal = False


	# TODO удалить
	@property
	def Z(self):
		return self.__Z

	# очистка АЛУ
	def clear(self):
		self.__Z.clear()
		# NEWIT обнуление флага равности и удаление ссылок сравнения регистров
		# self.__bigger = None
		# self.__smaller = None
		# self.__equal = False


	# IN: A - ссылка на регистр A
	# IN: B - ссылка на регистр B
	# IN: op - обрабатываемая операция
	def process(self, A: Registry, B: Registry, op: str):
		# очистка регистра перед вычислением (лучше бы после, чтобы не хранить значение)
		# NEWIT замена на очистку АЛУ, которая включает очистку регистра Z
		self.clear()
		if op == '+':
			# for digit in (A.value+B.value):# in self.add(A, B):
			# 	self.__Z.input(digit, self.__flags)
			self.__Z.value = A.value + B.value
		elif op == '-':
			# Тест сравнения
			# self.compare(A, B)
			# print('больше:', self.__bigger.name)
			# print('меньше:', self.__smaller.name)
			self.__Z.value = str(float(A.value) - float(B.value))
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

	# Вычисление максимальных длин целой и дробной частей
	# def __max_len(self, A: Registry, B: Registry):
	# 	return max(A.len_int, B.len_int), max(A.len_frac, B.len_frac)

	# генератор сложения (генерирует сбор строки числа)
	# IN: A - объект первого числа
	# IN: B - объект второго числа
	# def add(self, A: Registry, B: Registry):
	# 	# Вначале нужно найти максимально длинную часть
	# 	# max_len_int = max(A.len_int, B.len_int)
	# 	# max_len_frac = max(A.len_frac, B.len_frac)
	# 	max_len = self.__max_len(A, B)
	# 	carry = 0
	# 	# Генератор результата суммы
	# 	for x, y in zip(A.extract(*max_len), B.extract(*max_len)):
	# 		# Если попалась точка дробной части
	# 		if (x is None and A.comma) or (y is None and B.comma):
	# 			yield '.'
	# 		else:
	# 			sum = str(x + y + carry)
	# 			carry = 0
	# 			# если результат сложения с переносом
	# 			if len(sum) == 2:
	# 				carry, sum = 1, sum[1]
	# 			yield sum
	# 	if carry:
	# 		yield '1'
