# *****************************************************************************
# ПРОЕКТ:    GMP-CALCULATOR
# ФАЙЛ:      CALCULATOR.PY
# ЗАГОЛОВОК: КЛАСС КАЛЬКУЛЯТОРА
# ОПИСАНИЕ:  Описывает основной класс калькулятора и вспомогательных классов
# *****************************************************************************

import msvcrt
# DEPRECATED 06-06-2020 инициализация флагов в CPU
# import flags
import cpu
import display

class Calculator:
	""" ОСНОВНОЙ КЛАСС КАЛЬКУЛЯТОРА """
	# конструктор
	# IN: mode - режим отображения информации
	#            0 - тестовый, отображение регистров и флагов. Каждая операция оставляет строку
	#            1 - тестовый, отображение регистров и флагов как в 0, только одной строкой
	#            2 - рабочий, отображает только дисплей калькулятора
	#            3 - тестовый, отображение регистров и флагов, как в 0. Осуществляется возврат значения для pytest
	def __init__(self, mode: int=0):
		# NEWIT core ref регистры переносим в АЛУ
		# self.A = Registry('A') # регистр A
		# self.B = Registry('B') # регистр B
		# регистр Z теперь полностью принадлежит АЛУ, в калькуляторе его нет
		# DEPRECATED 06-06-2020 используем флаг PI (инициализируется в Flags)
		# self.OP = None        # текущее арифметическое действие
		# DEPRECATED 06-06-2020 флаги создаются в CPU
		# self.flags = flags.Flags()  # флаги калькулятора
		# DEPRECATED 06-06-2020 нет необходимости сохранять (используется в display)
		# self.mode = mode      # включение/выключения отладочного режима
		# в АЛУ добавляем ссылку на флаги, но сам АЛУ их не изменеят
		self.__CPU = cpu.CPU() # инициализация АЛУ
		# ссылка на флаги
		self.flags = self.__CPU.flags
		# Инициализация дисплея
		self.display = display.Display(self.__CPU, mode)
		# DEPRECATED 06-06-2020 вывод стартовой надписи из display
		# print("press 'q' to exit, 0-9 to enter value, 'ESC'-to clear, 'ENTER' to evaluate")
		self.displayRegisters()

	# общий сброс
	def clear(self):
		# NEWIT core ref очистка регистров происходит в АЛУ
		# self.A.clear()
		# self.B.clear()
		# очищаем АЛУ (фактически только регистр Z на данном этапе)
		self.__CPU.clear()
		# DEPRECATED 06-06-2020 используем PI (перенос во Flags)
		# self.OP = None
		# DEPRECATED 06-06-2020 очистка в CPU
		# self.flags.clear()

	# отобразить содержимое регистров в соответствии с выбранным режимом mode
	# NEWIT core ref изменение вывода регистров А и В
	def displayRegisters(self):
		if self.display.viewPrefix():
			print(self.display.viewPrefix(), end=self.display.getEnd())
		print(self.display.view(), end=self.display.getEnd())
		# if self.mode == 0:
		# 	print(f"A='{self.__CPU.A}'  ({self.__CPU.flags.PI})  B='{self.__CPU.B}'  Z='{self.__CPU.Z}'  SignZ='{self.__CPU.Z.sign}'  SignA='{self.__CPU.A.sign}'  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}")
		# elif self.mode == 1:
		# 	print("\r" + " "*50, end='\r')
		# 	print(f"A='{self.__CPU.A}'  ({self.__CPU.flags.PI})  B='{self.__CPU.B}'  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}", end="\r")
		# elif self.mode == 2:
		# 	print("\r" + " "*80, end="")
		# 	print("\r" + str(self.__CPU.A), end='')
		# изменился вид вывода (для возможности добавления новых значений)
		# elif self.mode == 3:
		# 	return (f"A='{self.__CPU.A}'  ({self.__CPU.flags.PI})  B='{self.__CPU.B}'"
		# 		f"  EQ={int(self.flags.EQ)}  CD={int(self.flags.CD)}  CONST={int(self.flags.CONST)}")

	# нажата цифровая клавиша. Ввод значения в регистр A
	# IN: с - символ нажатой клавиши
	# NEWIT core ref input и BS теперь в АЛУ
	def pressedDigitalKey(self, c: str):
		self.flags.equal_not_pressed()
		if c == '\x08':
			self.__CPU.BS()
		else:	
			self.__CPU.input(c)
			# NEWIT флаг заполнения регистра устанавливается, если 0 не является первым
			if self.flags.IS_NEW_INPUT and c != '0':
				self.flags.enable_reg_filling()

	# нажата арифметическая клавиша - обработаем
	# IN: с - символ нажатой клавиши
	def pressedOpcode(self, c: str):
		# NEWIT ввод отрицательного числа в калькуляторе организован как операция 0 - number
		self.flags.equal_not_pressed()
		# NEWIT опять вводим метод для обрезки незначащих 0 дробной части
		self.__CPU.truncate()
		# NEWIT core ref алгоритм выбора теперь полностью в АЛУ
		self.__CPU.process()
		self.__CPU.flags.PI = c
		self.flags.new_reg_filling()
		self.flags.enable_ops_continues()

	# нажата клавиша "равно" - обработаем
	def pressedEqual(self):
		self.flags.equal_pressed()
		self.__CPU.truncate()
		# NEWIT core ref алгоритм выбора теперь полностью в АЛУ
		self.__CPU.process()
		self.flags.new_reg_filling()
		self.flags.disable_ops_continues()

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
