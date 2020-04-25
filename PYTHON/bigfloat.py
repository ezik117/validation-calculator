# *****************************************************************************
# МОДУЛЬ:    bigfloat
# ФАЙЛ:      bigfloat.py
# ЗАГОЛОВОК: Классы больших чисел
# ОПИСАНИЕ:  Описывает класс больших чисел, используемых в регистрах
# *****************************************************************************

# Константы доступа к кортежу значений максимальных длин
_INTEGER, _FRACTION = range(2)

class BigFloat:

	def __init__(self):
		# Значение числа (строка, хотя можно сделать любой объект - список, файл)
		# TODO попробуем хранить, как и раньше, отдельно целую и дробную части
		# Определить 0 как пустые строки
		self.__integer = ''
		self.__fraction = ''
		# используется как переход от дробной к целой части и наоборот (для BS и input)
		self.__comma = False

# ----------------------------- Свойства ----------------------------- #

	# Запятая (разделитель) для переходов от одной части к другой части числа
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
		# если нет никаких значений, то не делаем ничего

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
		# NEWIT отправляется как маркер-разделитель целой и дробной части,
		# но наличие точки проверяется в методах АЛУ
		yield None
		# 4) генерирование целой части
		for digit in self.__integer[::-1]:
			yield int(digit)
		# 5) коррекция целой части (аналогично дробной (1))
		for _ in range(max_int - self.len_int):
			yield 0

	# Обрезка незначащих нулей дробной части
	def truncate(self):
		self.fraction = self.fraction.rstrip('0')

	# Вычисление максимальных длин целой и дробной частей
	# OUT: [0] - максимальная длина целой части
	# OUT: [1] - максимальная длина дробной части
	def __max_len(self, other):
		return max(self.len_int, other.len_int), max(self.len_frac, other.len_frac)

# ------------------------ Специальные методы ------------------------ #

	# Длина числа как длины целой и дробной части плюс 1 позиция точки (для совместимости с Registry)
	def __len__(self):
		return len(self.__integer) + int(self.__comma) + len(self.__fraction)
	
	# Метод равенства можно реализовать простым способом
	def __eq__(self, other):
		return self.integer == other.integer and self.fraction == other.fraction

	# Неравенство таким же способом не удается реализовать, т.к. требуется выравнивание
	def __lt__(self, other):
		max_len = self.__max_len(other)
		if (self.__integer.zfill(max_len[_INTEGER])
				< other.__integer.zfill(max_len[_INTEGER])):
			return True
		if ((self.__integer.zfill(max_len[_INTEGER])
					== other.__integer.zfill(max_len[_INTEGER]))
				and (self.__fraction.ljust(max_len[_FRACTION], '0')
					< other.__fraction.ljust(max_len[_FRACTION], '0'))):
			return True
		return False

	def __le__(self, other):
		return self == other or self < other

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

	# Для переопределения метода format
	def __format__(self, format_spec):
		return format(str(self), format_spec)

	# генератор сложения (генерирует сбор строки числа)
	# IN: A - объект первого числа
	# IN: B - объект второго числа
	def __operation(self, other, op):
		# Вначале нужно найти максимально длинную часть
		max_len = self.__max_len(other)
		if op == '-' and self < other:
			first = other.extract(*max_len)
			second = self.extract(*max_len)
		else:
			first = self.extract(*max_len)
			second = other.extract(*max_len)
		carry = 0
		pref = 1 if op == '+' else -1
		# Генератор результата суммы
		for x, y in zip(first, second):
			# Если попалась точка дробной части
			# BUG когда оба числа - целые
			# if (x is None and self.comma) or (y is None and other.comma):
			if x is None and y is None:
				yield ('.' if self.comma or other.comma else '')
				# yield '.'
			else:
				sum = str(x + pref * y + pref * carry)
				carry = 0
				# если результат сложения с переносом
				if len(sum) == 2:
					carry = 1
					sum = sum[1] if op == '+' else str(10 + int(sum))
				yield sum
		if op == '+' and carry:
			yield '1'

	def __add__(self, other):
		return self.__operation(other, '+')

	def __sub__(self, other):
		return self.__operation(other, '-')
