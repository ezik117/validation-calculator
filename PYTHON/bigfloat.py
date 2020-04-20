# *****************************************************************************
# МОДУЛЬ:    bigfloat
# ФАЙЛ:      bigfloat.py
# ЗАГОЛОВОК: Классы больших чисел
# ОПИСАНИЕ:  Описывает класс больших чисел, используемых в регистрах
# *****************************************************************************

class BigFloat:

	def __init__(self, reg):
		# Значение числа (строка, хотя можно сделать любой объект - список, файл)
		# TODO попробуем хранить, как и раньше, отдельно целую и дробную части
		# Определить 0 как пустые строки
		self.__integer = ''
		self.__fraction = ''
		# TODO нужно ли, если есть 2 части ???
		# можно использовать как переход от дробной к целой части и наоборот (для BS и input)
		self.__comma = False
		# NEWIT определение обработки входящих цифр (зависит от регистра)
		# self.__action = self.__influence(reg)

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

	# свойства для Registry
	@property
	def integer(self):
		return self.__integer

	@integer.setter
	def integer(self, val):
		self.__integer = val

	@property
	def fraction(self):
		return self.__fraction

	@fraction.setter
	def fraction(self, val):
		self.__fraction = val

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

	# IN: max_int - максимальная длина целой части числа из двух
	# IN: max_frac - максимальная длина дробной части числа из двух
	def extract(self, max_int: int = 0, max_frac: int = 0):
		# Начинаем с конца
		# 1) коррекция дробной части (len_frac либо равна, либо меньше max_frac)
		for _ in range(max_frac - self.len_frac):
			yield 0
		# 2) генерирование дробной части
		for digit in self.__fraction[::-1]:
			yield int(digit)
		# 3) точка
		# if self.__comma:
		# NEWIT отправляется как маркер-разделитель целой и дробной части,
		# но наличие точки проверяется в методах АЛУ
		yield None
		# 4) генерирование целой части
		for digit in self.__integer[::-1]:
			yield int(digit)
		#  затем целой, пропуская точку (с конца)
		# for idx in range(len(self._value)-1, -1, -1):
		# 	if idx > self.__len_int:
		# 		yield int(self._value[idx])
		# 	elif idx == self.len_int:
		# 		yield None
		# 	else:
		# 		yield int(self._value[idx])
		# 5) коррекция целой части (аналогично дробной (1))
		for _ in range(max_int - self.len_int):
			yield 0

	# Выбор метода обработки входящих цифр (в прямом для обычных регистров
	# или в обратном порядке для регистра Z)
	# def __influence(self, reg):
	# 	if reg == 'Z':
	# 		return lambda p, c: c + p
	# 	return lambda p, c: p + c

	# Определить метод вызова для присвоения значений числу
	# Изменение самого объекта при его вызове
	# def input(self, c):
	# 	# Ошибка при вводе второй точки
	# 	# TODO определить lambda для общих регистров и для Z
	# 	# или map ?
	# 	if c == '.' and self.comma:
	# 		raise ValueError("could not convert string to float: '{0}'".format(self._value + c))
	# 	if c == '.':
	# 		self.comma = True
	# 	elif self.comma:
	# 		self.__fraction = self.__action(self.__fraction, c)
	# 	# в том числе отсекает ввод незанчащих 0 целой части
	# 	# TODO заменить self.__integer на len == 0
	# 	elif self.__integer or c != '0':
	# 		self.__integer = self.__action(self.__integer, c)

# ------------------------ Специальные методы ------------------------ #

	# Длина числа как длины целой и дробной части плюс 1 позиция точки (для совместимости с Registry)
	def __len__(self):
		return len(self.__integer) + int(self.__comma) + len(self.__fraction)
	
	

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

	# Для метода format
	# def __format__(self, format_spec):
	# 	return format(str(self), format_spec)