# *****************************************************************************
# ПРОЕКТ:    GMP-CALCULATOR
# ФАЙЛ:      display.py
# ЗАГОЛОВОК: КЛАСС ДИСПЛЕЯ КАЛЬКУЛЯТОРА
# ОПИСАНИЕ:  Описывает класс дисплея калькулятора
# *****************************************************************************

class Display():

	def __init__(self, cpu, mode: int=0):
		# Ссылка на класс процессора, в котором расположены регистры
		# В данном случае нам нужны только значения регистров
		self.__CPU = cpu
		# начальный вывод на экран теперь происходит при инициализации дисплея
		print("press 'q' to exit, 0-9 to enter value, 'ESC'-to clear, 'ENTER' to evaluate")

	def __setting(self, mode):
		modes = {
			'A': {
				'value': True,
				'sign': True,
				'comma': True
			},
			'B': {
				'value': True,
				'sign': True,
				'comma': True
			},
			'Z': {
				'value': True,
				'sign': True,
				'comma': True
			}
		}