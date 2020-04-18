# *****************************************************************************
# МОДУЛЬ:    GMP-CALCULATOR
# ФАЙЛ:      CALCULATOR.PY
# ЗАГОЛОВОК: КЛАСС КАЛЬКУЛЯТОРА
# ОПИСАНИЕ:  Описывает основной класс калькулятора и вспомогательных классов
# *****************************************************************************

import msvcrt
from registers import Registry
import flags
import ALU

# FIXME ТЗ устарело
# TODO реконструкция калькулятора
# Реализация:
# - [x] добавить возможность ввода точки для дробных величин
# TODO перемещение флага в регистры
# - [-] ??? нужен ли флаг введенной точки (вынесен в класс Registry)

class Calculator:
	""" ОСНОВНОЙ КЛАСС КАЛЬКУЛЯТОРА """
	# конструктор
	# IN: mode - режим отображения информации
	#            0 - тестовый, отображение регистров и флагов. Каждая операция оставляет строку
	#            1 - тестовый, отображение регистров и флагов как в 0, только одной строкой
	#            2 - рабочий, отображает только дисплей калькулятора
	#            3 - тестовый, отображение регистров и флагов, как в 0. Осуществляется возврат значения для pytest
	def __init__(self, mode: int=0):
		self.A = Registry('A') # регистр A
		self.B = Registry('B') # регистр B
		# регистр Z теперь полностью принадлежит АЛУ, в калькуляторе его нет
		self.OP = None        # текущее арифметическое действие
		self.flags = flags.Flags()  # флаги калькулятора
		self.mode = mode      # включение/выключения отладочного режима
		# в АЛУ добавляем ссылку на флаги, но сам АЛУ их не изменеят
		self.__ALU = ALU.ALU(self.flags) # инициализация АЛУ
		print("press 'q' to exit, 0-9 to enter value, 'ESC'-to clear, 'ENTER' to evaluate")
		self.displayRegisters()

	# общий сброс
	def clear(self):
		self.A.clear()
		self.B.clear()
		# очищаем АЛУ (фактически только регистр Z на данном этапе)
		self.__ALU.clear()
		self.OP = None
		self.flags.clear()

	# отобразить содержимое регистров в соответствии с выбранным режимом mode
	def displayRegisters(self):
		if self.mode == 0:
			print(f"A='{self.A}'  ({self.OP})  B='{self.B}'  Z='{self.__ALU.Z}'  CommaZ={self.__ALU.Z.comma}  CommaA={self.A.comma}  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}")
		elif self.mode == 1:
			print("\r" + " "*50, end='\r')
			print(f"A='{self.A}'  ({self.OP})  B='{self.B}'  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}", end="\r")
		elif self.mode == 2:
			print("\r" + " "*80, end="")
			print("\r" + self.A, end='')
		# изменился вид вывода (для возможности добавления новых значений)
		elif self.mode == 3:
			return (f"A='{self.A}'  ({self.OP})  B='{self.B}'"
				f"  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}")

	# нажата цифровая клавиша. Ввод значения в регистр A
	# IN: с - символ нажатой клавиши
	def pressedDigitalKey(self, c: str):
		self.flags.EQUAL_NOT_PRESSED
		if c == '\x08':
			self.A.BS()
		else:	
			self.A.input(c, self.flags)
			self.flags.ENABLE_REG_FILLING

	# нажата арифметическая клавиша - обработаем
	# IN: с - символ нажатой клавиши
	def pressedOpcode(self, c: str):
		self.flags.EQUAL_NOT_PRESSED
		self.A.prepare()
		if self.flags.IS_OPERATON_POSSIBLE:
			self.__ALU.process(self.B, self.A, self.OP)
		self.B.copyFrom(self.A)
		self.OP = c
		self.flags.NEW_REG_FILLING
		self.flags.ENABLE_OPS_CONTINUES

	# нажата клавиша "равно" - обработаем
	def pressedEqual(self):
		self.flags.EQUAL_PRESSED
		self.A.prepare()
		if self.flags.IS_OPS_CONTINUES:
			self.__ALU.process(self.B, self.A, self.OP)
		else:
			self.__ALU.process(self.A, self.B, self.OP)
		self.flags.NEW_REG_FILLING
		self.flags.DISABLE_OPS_CONTINUES

	# цикл обработки нажатия клавиш с клавиатуры
	def processKeys(self):
		while (True):
			if msvcrt.kbhit():
				c = msvcrt.getch().decode()

				# quit
				if c == 'q':
					break

				# digital keys
				if c in set('0123456789.') or (c == '\x08'):
					self.pressedDigitalKey(c)
				# reset key
				elif c == '\x1B':
					self.clear()
				# opcode keys
				elif c in ['+', '-', '*', '/']:
					self.pressedOpcode(c)
				# equal key
				elif c == '\x0D':
					self.pressedEqual()

				self.displayRegisters()
