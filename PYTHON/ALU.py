from registers import Registry, RegistryZ

# TODO реконструкция ALU
# Причины:
# 1) необходимо реализовать математическую логику для 4 действий (+-/*)
# Реализация:
# 1) Получить 2 части числа через генератор yield ???
# Можно будет сразу собирать результат и отдавать, чтобы не хранить его
# 2) Для этого нужно знать длину каждой части, чтобы выравнивать их


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

	# TODO очистка АЛУ
	def clear(self):
		self.__Z.clear()


	# IN: A - ссылка на регистр A
	# IN: B - ссылка на регистр B
	# IN: op - обрабатываемая операция
	def process(self, A: Registry, B: Registry, op: str):
		# NEWIT очистка регистра перед вычислением (лучше бы после, чтобы не хранить значение)
		self.__Z.clear()
		if op == '+':
			# NEWIT новое вычисление через генераторы
			for digit in self.add(A, B):
				# NEWIT и использование переопределенного метода input для регистра Z
				self.__Z.input(digit, self.__flags)
		elif op == '-':
			self.__Z.value = str(float(A.value) - float(B.value))
		elif op == '/':
			self.__Z.value = str(float(A.value) / float(B.value))
		elif op == '*':
			self.__Z.value = str(float(A.value) * float(B.value))
		else:
			return  # нет операции
		# KILLME Убрать в будущем (используется временно, т.к. не все операции реализуются через input)
		if self.__Z.value.find('.') != -1:
			self.__Z.comma = True
		# NEWIT очистка от незначащих нулей используется в любом случае
		self.__Z.prepare()
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

	# NEWIT генератор сложения (генерирует сбор строки числа)
	# IN: A - объект первого числа
	# IN: B - объект второго числа
	def add(self, A: Registry, B: Registry):
		# Вначале нужно найти максимально длинную часть
		max_len_int = max(A.len_int, B.len_int)
		max_len_frac = max(A.len_frac, B.len_frac)
		carry = 0
		# Генератор результата суммы
		for x, y in zip(A.extract(max_len_int, max_len_frac),
						B.extract(max_len_int, max_len_frac)):
			# Если попалась точка дробной части
			if x is None and y is None:
				yield '.'
			else:
				sum = str(x + y + carry)
				carry = 0
				# если результат сложения с переносом
				if len(sum) == 2:
					carry, sum = 1, sum[1]
				yield sum
		if carry:
			yield '1'
