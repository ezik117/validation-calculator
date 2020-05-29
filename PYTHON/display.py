# *****************************************************************************
# ПРОЕКТ:    GMP-CALCULATOR
# ФАЙЛ:      display.py
# ЗАГОЛОВОК: КЛАСС ДИСПЛЕЯ КАЛЬКУЛЯТОРА
# ОПИСАНИЕ:  Описывает класс дисплея калькулятора
# *****************************************************************************

class Display():

	# список регистров, выводимых в соответствующем режиме работы калькулятора
	__modes = ['ABZ', 'AB', 'A', 'AB']

	def __init__(self, cpu, mode: int=0):
		# Ссылка на класс процессора, в котором расположены регистры
		# В данном случае нам нужны только значения регистров
		self.__CPU = cpu
		self.__mode = mode
		self.model = self.__setting(mode)
		# начальный вывод на экран теперь происходит при инициализации дисплея
		print("press 'q' to exit, 0-9 to enter value, 'ESC'-to clear, 'ENTER' to evaluate")

# ------------------------------ Viewers ----------------------------- #

	# @property
	# def viewA(self):
	# 	return f"A='{self.__CPU.A}'"

	# @property
	# def viewB(self):
	# 	return f"B='{self.__CPU.B}'"

	# @property
	# def viewZ(self):
	# 	return f"Z='{self.__CPU.Z}'"
	@property
	def flagCD(self):
		return f"CD={int(self.__CPU.flags.CD)}"

	@property
	def flagCONST(self):
		return f"CONST={int(self.__CPU.flags.CONST)}"

	@property
	def flagEQ(self):
		return f"EQ={int(self.__CPU.flags.EQ)}"

	def flags(self):
		return '  '.join((self.flagCD, self.flagCONST, self.flagEQ))

	def comma(self, reg):
		return f"Comma{reg}='{self.__CPU.name(reg).comma}'"

	def viewReg(self, reg):
		return f"{reg}='{self.__CPU.name(reg)}'"

	def sign(self, reg):
		return f"Sign{reg}='{self.__CPU.name(reg).sign}'"

	# сборка отображения
	def view(self):
		return '  '.join((self.viewReg(reg) for reg in Display.__modes[self.__mode]))

	def __setting(self, mode):
		regs = {}
		for reg in self.__CPU.get_regnames():
			regs.setdefault(reg, {
				'value': True,
				'sign': True,
				'comma': True
			})
		return regs

