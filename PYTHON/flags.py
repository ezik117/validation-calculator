# *****************************************************************************
# МОДУЛЬ:    flags
# ФАЙЛ:      flags.py
# ЗАГОЛОВОК: КЛАСС ФЛАГОВ (ДЛЯ КАЛЬКУЛЯТОРА)
# ОПИСАНИЕ:  Описывает класс фдагов калькулятора
# *****************************************************************************

class Flags:
	""" КЛАСС ДЛЯ ФЛАГОВ КАЛЬКУЛЯТОРА """

	def __init__(self):
		# clear display, 1-означает что новый ввод в A затрет старые результаты
		# , а так же в комбинации с OP=1, что в А есть число
		# , 0-ввод в регистр А разрешен
	 	# бит 0:
		self.__CD = True
		# constant, 1-означает незавершенную операцию. Незавершенная операция, это последовательный
		# ввод арифметических действий, пока не будет нажата EQ. В случае незавершенной операции
		# вычисления ведуться как B op A. Если операция завершена, то предполагается что второго операнда
		# нет и он берется из регистра В, и соответственно рассчитывается как A op B.
		# Используется для выбора алгоритма АЛУ.
	 	# бит 1:
		self.__CONST = False
		# equal - нажата ли клавиша "равно". Используется для выбора алгоритма АЛУ.
		# бит 2:
		self.__EQ = False


# -------------------------------------------------------------------- #
#                               Свойства                               #
# -------------------------------------------------------------------- #

# ------------------------ Временные свойства ------------------------ #

	# Эти свойства необходимы для время перевода калькулятора на новый класс Flags
	# TODO геттеры пока остаются для поддержки вывода на экран и в pytest
	@property
	def CD(self):
		return self.__CD
	
	# @CD.setter
	# def CD(self, val):
	# 	self.__CD = val

	@property
	def CONST(self):
		return self.__CONST
	
	# @CONST.setter
	# def CONST(self, val):
	# 	self.__CONST = val
	
	@property
	def EQ(self):
		return self.__EQ
	
	# @EQ.setter
	# def EQ(self, val):
	# 	self.__EQ = val

# ------------------------------ Флаг CD ----------------------------- #

	# Заполняем текущий регистр А ?
	@property
	def IS_REG_FILLING(self):
		return not self.__CD

	# Вводим новое число ?
	@property
	def IS_NEW_INPUT(self):
		return self.__CD

	# Разрешить новый ввод
	# @property
	def new_reg_filling(self):
		self.__CD = True

	# Заполнить текущий регистр А
	# @property
	def enable_reg_filling(self):
		self.__CD = False

# ---------------------------- Флаг CONST ---------------------------- #

	# Цикл ввода операций продолжается ?
	@property
	def IS_OPS_CONTINUES(self):
		return self.__CONST

	# Цикл ввода операций остановлен ?
	@property
	def IS_OPS_STOPPED(self):
		return not self.__CONST

	# Начать новый цикл ввода операций
	# @property
	def enable_ops_continues(self):
		self.__CONST = True

	# Закончить текущий цикл ввода операций
	# @property
	def disable_ops_continues(self):
		self.__CONST = False

# ------------------------------ Флаг EQ ----------------------------- #

	# Клавиша "равно" нажата ?
	@property
	def IS_EQUAL_PRESSED(self):
		return self.__EQ

	# Запомнить событие нажатия клавиши "равно"
	# @property
	def equal_pressed(self):
		self.__EQ = True

	# Запомнить, что клавиша "равно" еще не нажата
	# @property
	def equal_not_pressed(self):
		self.__EQ = False

# -------------------- проверка для pressedOpcode -------------------- #

	# Возможно ли сейчас провести операцию ?
	@property
	def IS_OPERATON_POSSIBLE(self):
		return self.IS_REG_FILLING and self.IS_OPS_CONTINUES

# ----------------------- Комбинации работы ALU ---------------------- #

	# Операция вида B op A ?
	@property
	def IS_B_op_A(self):
		return self.IS_EQUAL_PRESSED and self.IS_OPS_CONTINUES

	# Операция вида A op B ?
	@property
	def IS_A_op_B(self):
		return self.IS_EQUAL_PRESSED and self.IS_OPS_STOPPED

	# Операции продолжаются друг за другом ?
	@property
	def IS_NEXT_OPERATION(self):
		return not self.IS_EQUAL_PRESSED and self.IS_OPS_CONTINUES

# -------------------------------------------------------------------- #
#                                Методы                                #
# -------------------------------------------------------------------- #

	def clear(self):
		self.new_reg_filling()
		self.disable_ops_continues()
		self.equal_not_pressed()


# -------------------------- Тестовые методы ------------------------- #

	def check(self):
		return self.__CD, self.__CONST, self.__EQ
	
	def control(self):
		return str(int(self.__EQ)) + str(int(self.__CD)) + str(int(self.__CONST))
