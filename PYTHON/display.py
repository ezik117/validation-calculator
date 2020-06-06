# *****************************************************************************
# ПРОЕКТ:    GMP-CALCULATOR
# ФАЙЛ:      display.py
# ЗАГОЛОВОК: КЛАСС ДИСПЛЕЯ КАЛЬКУЛЯТОРА
# ОПИСАНИЕ:  Описывает класс дисплея калькулятора
# *****************************************************************************

class Display():

	# список регистров, выводимых в соответствующем режиме работы калькулятора
	__modes = ['BZ', 'B', '', 'B']
	# управляющие символы (конец строки) для разных режимов работы
	__carriage = ['\n', '\r', '', '\n']
	# строки стирания для разных режимов, если они есть
	__erasure = ["", "\r" + " "*80, "\r" + " "*80, ""]

	def __init__(self, cpu, mode: int=0):
		# Ссылка на класс процессора, в котором расположены регистры
		# В данном случае нам нужны только значения регистров
		self.__CPU = cpu
		self.__mode = mode
		# значение для параметра end в функции print
		self.__end = Display.__carriage[mode]
		# self.model = self.__setting(mode)
		# начальный вывод на экран теперь происходит при инициализации дисплея
		print("press 'q' to exit, 0-9 to enter value, 'ESC'-to clear, 'ENTER' to evaluate")

# ------------------------------ Viewers ----------------------------- #

	# возврат параметра end для функции print()
	def getEnd(self):
		return self.__end

	# отображение строки флагов CD, CONST, EQ и их значений
	def viewFlags(self):
		return '  '.join([f"{flag}={int(getattr(self.__CPU.flags, flag))}"
									for flag in ['EQ', 'CD', 'CONST']])

	# отображение значений регистров в зависимости от схемы отображения (кроме А)
	def viewExtraRegs(self):
		return '  '.join((f"{reg}='{self.__CPU.name(reg)}'" for reg in Display.__modes[self.__mode]))

	# отображение регистра А
	def viewRegA(self):
		if self.__mode == 2:
			return f"{self.__CPU.name('A')}"
		else:
			return f"A='{self.__CPU.name('A')}'"

	# отображение математической операции (флаг PI)
	def viewPI(self):
		return f"({self.__CPU.flags.PI})"

	# отображение префикса
	def viewPrefix(self):
		return self.__erasure[self.__mode]

	# TODO 06-06-2020 отображение запятой и знака
	# def comma(self, reg):
	# 	return f"Comma{reg}='{self.__CPU.name(reg).comma}'"

	# def sign(self, reg):
	# 	return f"Sign{reg}='{self.__CPU.name(reg).sign}'"

	# общий вид (пока регистры и флаги)
	def view(self):
		if self.__mode == 2:
			return "\r" + self.viewRegA()
		else:
			return '  '.join((self.viewRegA(), self.viewPI(), self.viewExtraRegs(), self.viewFlags()))

	# TODO 06-06-2020 режимы отображения знаков и запятых
	# def __setting(self, mode):
	# 	regs = {}
	# 	for reg in self.__CPU.get_regnames():
	# 		regs.setdefault(reg, {
	# 			'value': True,
	# 			'sign': True,
	# 			'comma': True
	# 		})
	# 	return regs
