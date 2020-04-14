# *****************************************************************************
# МОДУЛЬ:    GMP-CALCULATOR
# ФАЙЛ:      REGISTERS.PY
# ЗАГОЛОВОК: КЛАССЫ РЕГИСТРОВ
# ОПИСАНИЕ:  Описывает класс регистров калькулятора
# *****************************************************************************

# TODO реконструкция регистра
# Причины:
# 1) нет смысла хранить несколько объектов отдельно (в классах Registry и BigFloat).
# Это растрата памяти, что плохо для ресурсозатратного проекта с расчетом больших чисел.
# Реализация:
# - [x] специальный метод str() для реализации вывода результата в виде строки
# - [x] закрыть атрибут value и сделать его видимым через декоратор свойства
# - [x] ??? установить setter для свойства value, если это регистр Z (спорно, т.к. другие регистры будут возвращать ошибку)
# TODO вынести в класс Calculator:
# - [-] установить ограничительные множества цифр (decimal, octal и т.п.) для проверки соответствия ввода
# TODO пока храним строку полностью:
# - [-] разделить хранение целой и дробной частей, т.к. невозможно работать с типом float без потери точности
# - [ ] ??? добавить свойства получения длин каждой части (необходимо для дальнейших расчетов)
# - [x] исправить метод input() для возможности ввода дробных величин
# - [x] ??? ограничение ввода незначащих нулей для дробной части
# ------------
# Реализация 2:
# 1) Узнать длину каждой части через find ?
# 2) Запомнить их в свойствах

class Regisry:
	""" КЛАСС ДЛЯ РЕГИСТРА КАЛЬКУЛЯТОРА """
	# конструктор
	# IN: name - буква регистра, необходима для избежания получения одинаковой ссылки на
	#            разные объекты
	# IN: base - ссылка на базовый класс калькулятора для 
	def __init__(self, name: str):
		# NEWIT закрыть изменение имени регистра извне
		self.__name = name  # буква регистра
		# NEWIT закрыть изменение значения регистра извне напрямую (кроме регистра Z)
		self.__value = '0'  # значение регистра как строка
		# NEWIT флаг ввода точки
		self.__comma = False # событие ввода точки
		# Длины каждой части
		self.__len_int = 0
		self.__len_frac = 0

# -------------------------- Свойства класса ------------------------- #

	# NEWIT getter значения регистра
	@property
	def value(self):
		return self.__value

	# NEWIT setter регистра Z
	@value.setter
	def value(self, value):
		if self.__name == 'Z':
			self.__value = value
		else:
			raise ValueError("Registry: unable to set value for registry '{}'".format(self.__name))

	# TODO можно удалить в будущем (для тестов)
	@property
	def comma(self):
		return int(self.__comma)

	@comma.setter
	def comma(self, value):
		if self.__name == 'Z':
			self.__comma = value
		else:
			raise ValueError("Registry: unable to set value for registry '{}'".format(self.__name))

# --------------------------- Методы класса -------------------------- #

	# сброс содержимого регистра
	def clear(self):
		self.__value = '0'
		# NEWIT сброс флага запятой при очистке
		self.__comma = False
		self.__len_int = 0
		self.__len_frac = 0

	# затереть один символ с конца
	def BS(self):
		if len(self.__value) > 1:
			# NEWIT сброс флага запятой, если она затерта
			if self.__value[-1] == '.':
				self.__comma = False
			self.__value = self.__value[:-1]
		else:
			self.__value = '0'

	# ввести один символ в конец
	# IN: c - цифра или точка в строковом представлении
	# IN: newInput - если True, то содержимое регистра заменяется новым значением в 'c'
	#              - если False, то значение в 'c' добавляется в конец значения регистра
	def input(self, c: str, flags: object):
		# NEWIT Если новый ввод, то сброс флага запятой
		if flags.IS_NEW_INPUT: self.__comma = False
		# NEWIT защита от ввода второй запятой
		# if c == '.' and flags.IS_REG_FILLING and '.' in self.__value:
		if c == '.' and flags.IS_REG_FILLING and self.__comma:
			raise ValueError("could not convert string to float: '{0}'".format(self.__value + c))
		# NEWIT поднятие флага запятой, если введена запятая
		if c == '.': self.__comma = True
		if (len(self.__value) == 1 and self.__value == "0") or flags.IS_NEW_INPUT:
			self.__value = c
		else:
			self.__value += c

	# копирует значение из другого регистра класса Regisry
	def copyFrom(self, R:'Regisry'):
		self.__value = R.value
		# NEWIT копирование флага запятой
		self.__comma = R.__comma
		# TODO нужно будет копировать длины частей
		self.__len_int = R.__len_int
		self.__len_frac = R.__len_frac

	# NEWIT Работа метода:
	# 1) удаление незначащих нулей дробной части
	# 2) определение длин целой и дробной частей
	# TODO не протестировано в pytest
	def prepare(self):
		if self.__comma:
			self.__value = self.__value.rstrip('0')
			if self.__value.endswith('.'):
				self.__value += '0'
			self.__len_int = self.__value.find('.')
			self.__len_frac = len(self.__value) - self.__len_int - 1
		else:
			self.__len_int = len(self.__value)
			self.__len_frac = 0
		# print(self.__len_int, self.__len_frac)


# ------------------------ Специальные методы ------------------------ #

	# TODO переделать, когда будут дробные числа
	def __str__(self):
		return self.__value
