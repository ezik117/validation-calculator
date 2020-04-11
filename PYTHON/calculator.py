# *****************************************************************************
# МОДУЛЬ:    GMP-CALCULATOR
# ФАЙЛ:      CALCULATOR.PY
# ЗАГОЛОВОК: КЛАСС КАЛЬКУЛЯТОРА
# ОПИСАНИЕ:  Описывает основной класс калькулятора и вспомогательных классов
# *****************************************************************************

import msvcrt
from registers import Regisry
import ALU


class Flags:
	""" КЛАСС ДЛЯ ФЛАГОВ КАЛЬКУЛЯТОРА """
	def __init__(self):
		# clear display, 1-означает что новый ввод в A затрет старые результаты
		# , а так же в комбинации с OP=1, что в А есть число
		# , 0-ввод в регистр А разрешен
		self.CD = True
		# constant, 1-означает незавершенную операцию. Незавершенная операция, это последовательный
		# ввод арифметических действий, пока не будет нажата EQ. В случае незавершенной операции
		# вычисления ведуться как B op A. Если операция завершена, то предполагается что второго операнда
		# нет и он берется из регистра В, и соответственно рассчитывается как A op B.
		# Используется для выбора алгоритма АЛУ.
		self.CONST = False
		# equal - нажата ли клавиша "равно". Используется для выбора алгоритма АЛУ.
		self.EQ = False
	def clear(self):
		self.CD = True
		self.CONST = False
		self.EQ = False


# TODO реконструкция калькулятора
# Реализация:
# - [ ] добавить возможность ввода точки для дробных величин
# - [ ] ??? нужен ли флаг введенной точки

class Calculator:
	""" ОСНОВНОЙ КЛАСС КАЛЬКУЛЯТОРА """
	# конструктор
	# IN: mode - режим отображения информации
	#            0 - тестовый, отображение регистров и флагов. Каждая операция оставляет строку
	#            1 - тестовый, отображение регистров и флагов как в 0, только одной строкой
	#            2 - рабочий, отображает только дисплей калькулятора
	def __init__(self, mode: int=0):
		self.A = Regisry('A') # регистр A
		self.B = Regisry('B') # регистр B
		# NEWIT регистр Z теперь полностью принадлежит АЛУ, в калькуляторе его нет
		self.OP = None        # текущее арифметическое действие
		self.flags = Flags()  # флаги калькулятора
		self.mode = mode      # включение/выключения отладочного режима
		# NEWIT в АЛУ добавляем ссылку на флаги, но сам АЛУ их не изменеят
		self.__ALU = ALU.ALU(self.flags) # инициализация АЛУ
		print("press 'q' to exit, 0-9 to enter value, 'ESC'-to clear, 'ENTER' to evaluate")
		self.displayRegisters()

	# общий сброс
	def clear(self):
		self.A.clear()
		self.B.clear()
		# NEWIT очищаем АЛУ (фактически только регистр Z на данном этапе)
		self.__ALU.clear()
		self.OP = None
		self.flags.clear()

	# отобразить содержимое регистров в соответствии с выбранным режимом mode
	def displayRegisters(self):
		if self.mode == 0:
			print(f"A='{self.A}'  ({self.OP})  B='{self.B}'  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}")
		elif self.mode == 1:
			print("\r" + " "*50, end='\r')
			print(f"A='{self.A}'  ({self.OP})  B='{self.B}'  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}", end="\r")
		elif self.mode == 2:
			print("\r" + " "*80, end="")
			print("\r" + self.A, end='')

	# нажата цифровая клавиша. Ввод значения в регистр A
	# IN: с - символ нажатой клавиши
	def pressedDigitalKey(self, c: str):
		if c == '\x08':
			self.A.BS()
		else:	
			self.A.input(c, self.flags.CD)
			self.flags.CD = False

	# нажата арифметическая клавиша - обработаем
	# IN: с - символ нажатой клавиши
	def pressedOpcode(self, c: str):
		if not self.flags.CD:
			if self.flags.CONST:
				# NEWIT теперь обработка такокго вида:
				self.__ALU.process(self.B, self.A, self.OP)
		self.B.copyFrom(self.A)
		self.OP = c
		self.flags.CD = True
		self.flags.CONST = True

	# нажата клавиша "равно" - обработаем
	def pressedEqual(self):
		if self.flags.CONST:
			# NEWIT см. выше
			self.__ALU.process(self.B, self.A, self.OP)
		else:
			# NEWIT см. выше
			self.__ALU.process(self.A, self.B, self.OP)

		self.flags.CD = True
		self.flags.CONST = False

	# цикл обработки нажатия клавиш с клавиатуры
	def processKeys(self):
		while (True):
			if msvcrt.kbhit():
				c = msvcrt.getch().decode()

				# quit
				if c == 'q':
					break

				# digital keys
				if ('0' <= c <= '9') or (c == '\x08'):
					self.flags.EQ = False
					self.pressedDigitalKey(c)
				# reset key
				elif c == '\x1B':
					self.clear()
				# opcode keys
				elif c in ['+', '-', '*', '/']:
					self.flags.EQ = False
					self.pressedOpcode(c)
				# equal key
				elif c == '\x0D':
					self.flags.EQ = True
					self.pressedEqual()

				self.displayRegisters()

# NEWIT АЛУ вынесен в отдельный класс