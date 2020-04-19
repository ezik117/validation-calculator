# *****************************************************************************
# МОДУЛЬ:    bigfloat
# ФАЙЛ:      bigfloat.py
# ЗАГОЛОВОК: Классы больших чисел
# ОПИСАНИЕ:  Описывает класс больших чисел, используемых в регистрах
# *****************************************************************************

class BigFloat:

	def __init__(self):
		# Значение числа (строка, хотя можно сделать любой объект - список, файл)
		# TODO попробуем хранить, как и раньше, отдельно целую и дробную части
		# Определить 0 как пустые строки
		self.__integer = ''
		self.__fraction = ''
		# TODO нужно ли, если есть 2 части ???
		# можно использовать как переход от дробной к целой части и наоборот (для BS и input)
		self.__comma = False
		# TODO также нужны ли длины частей, если обе части разделены ???

# ----------------------------- Свойства ----------------------------- #

	# Запятая (разделитель) для переходов от части к части числа
	@property
	def comma(self):
		return self.__comma
	
	@comma.setter
	def comma(self, val):
		self.__comma = val

	# свойства частей длины
	@property
	def len_int(self):
		return len(self.__integer)

	@property
	def len_frac(self):
		return len(self.__fraction)

# ------------------------------ Методы ------------------------------ #

	# метод затирания последнего символа числа (какой магический ?)
	def BS(self):
		if self.__fraction:
			self.__fraction = self.__fraction[:-1]
		elif self.comma:
			self.__comma = False
		elif self.__integer:
			self.__integer = self.__integer[:-1]
		# есои нет никаких значений, то не делаем ничего

# ------------------------ Специальные методы ------------------------ #

	# Длина числа как длины целой и дробной части плюс 1 позиция точки (для совместимости с Registry)
	def __len__(self):
		return len(self.__integer) + int(self.__comma) + len(self.__fraction)
	
	# Определить метод вызова для присвоения значений числу
	# Изменение самого объекта при его вызове
	def __call__(self, c):
		# Ошибка при вводе второй точки
		if c == '.' and self.comma:
			raise ValueError("could not convert string to float: '{0}'".format(self._value + c))
		if c == '.':
			self.comma = True
		elif self.comma:
			self.__fraction += c
		# в том числе отсекает ввод незанчащих 0 целой части
		elif self.__integer or c != '0':
			self.__integer += c

	# Строковое представление:
	# 1) если ничего не введено, то выводит 0
	# 2) если введено целое число, показывает целое число
	# 3) если введена точка, показывает дробное число
	# 4) если дробной части нет, но есть точка, показывает "х.0" или "0.0"
	def __str__(self):
		comma = '.' if self.comma else ''
		integer = '0' if self.comma and not self.__integer else self.__integer
		frac = '0' if self.comma and not self.__fraction else self.__fraction
		# если нужен ноль с точкой, можно переделать
		return (integer + comma + frac) if len(self) else '0'
