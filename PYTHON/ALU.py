
from registers import Regisry

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
		self.__Z = Regisry('Z')  # симуляция регистра АЛУ


	# TODO удалить
	@property
	def Z(self):
		return self.__Z

	# TODO очистка АЛУ
	def clear(self):
		self.__Z.clear()


	# IN: A - ссылка на регистр A
	# IN: B - ссылка на регистр B
	def process(self, A: Regisry, B: Regisry, op: str):
		if op == '+':
			self.__Z.value = str(float(A.value) + float(B.value))
		elif op == '-':
			self.__Z.value = str(float(A.value) - float(B.value))
		elif op == '/':
			self.__Z.value = str(float(A.value) / float(B.value))
		elif op == '*':
			self.__Z.value = str(float(A.value) * float(B.value))
		else:
			return  # нет операции
		# TODO (future ?) после вычисления нет информации о точке, на которой основываются расчеты
		if self.__Z.value.find('.') != -1:
			self.__Z.comma = True
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
