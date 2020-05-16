# *****************************************************************************
# МОДУЛЬ:    bigfloat
# ФАЙЛ:      bigfloat.py
# ЗАГОЛОВОК: Классы больших чисел
# ОПИСАНИЕ:  Описывает класс больших чисел, используемых в регистрах
# *****************************************************************************

class BigFloat:

	# NEWIT Атрибуты класса
	__STRAIGHT, __INVERSE = 1, -1

	def __init__(self):
		# Значение числа (строка, хотя можно сделать любой объект - список, файл)
		# TODO попробуем хранить, как и раньше, отдельно целую и дробную части
		# Определить 0 как пустые строки
		self.__integer = ''
		self.__fraction = ''
		# используется как переход от дробной к целой части и наоборот (для BS и input)
		self.__comma = ''
		# NEWIT знак числа: "-" - отрицательное число, интерпретируется как True
		# "" - положительное число, интерпретируется как False (пустая строка)
		self.__sign = ''

# ----------------------------- Свойства ----------------------------- #

	# Запятая (разделитель) для переходов от одной части к другой части числа
	@property
	def comma(self):
		return self.__comma
	
	@comma.setter
	def comma(self, val):
		self.__comma = val

	# Знак числа
	@property
	def sign(self):
		return self.__sign
	
	@sign.setter
	def sign(self, val):
		self.__sign = val

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
			self.__comma = ''
		elif self.__integer:
			self.__integer = self.__integer[:-1]
		# если нет никаких значений, то не делаем ничего

	# IN: max_int - максимальная длина целой части числа из двух
	# IN: max_frac - максимальная длина дробной части числа из двух
	# IN: first - направление обхода числа (True - обход с начала, False - обход с конца)
	def extract(self, max_int: int = 0, max_frac: int = 0, direct: int = __INVERSE):
		# NEWIT Определяем переменные для обхода (кортежи, из которых выбираются
		# данные согласно направлению обхода direct)
		max_diff = None, max_int - self.len_int, max_frac - self.len_frac
		num_parts = None, self.__integer, self.__fraction
		# 0) знак числа в прямом порядке (только для методов сравнения)
		if direct == 1:
			yield self.sign
		# 1) коррекция дробной части (len_frac либо равна, либо меньше max_frac)
		for _ in range(max_diff[direct]):
			yield 0
		# 2) генерирование дробной части
		for digit in (num_parts[direct][::direct]):
			yield int(digit)
		# 3) точка
		# NEWIT отправляется как маркер-разделитель целой и дробной части,
		# но наличие точки проверяется в методах АЛУ
		if direct == -1:
			yield None
		# 4) генерирование целой части
		for digit in (num_parts[-direct][::direct]):
			yield int(digit)
		# 5) коррекция целой части (аналогично дробной (1))
		for _ in range(max_diff[-direct]):
			yield 0

	# Обрезка незначащих нулей дробной части
	def truncate(self):
		self.fraction = self.fraction.rstrip('0')

	# Вычисление максимальных длин целой и дробной частей
	# OUT: [0] - максимальная длина целой части
	# OUT: [1] - максимальная длина дробной части
	def __max_len(self, other):
		return max(self.len_int, other.len_int), max(self.len_frac, other.len_frac)

	# NEWIT Конвертирование типов int и float в BigFloat для сравнения
	def __convert_type(self, other):
		X = BigFloat()
		if str(other)[0] == '-':
			X.sign = '-'
			other = str(other)[1:]
		if str(other)[0] == '+':
			other = str(other)[1:]
		if '.' in str(other): X.comma = '.'
		X.integer, *X.fraction = str(other).split('.')
		X.integer = X.integer.lstrip('0')
		X.fraction = X.fraction[0].rstrip('0') if X.fraction else ''
		return X

# ------------------------ Специальные методы ------------------------ #

	# Длина числа как длины целой и дробной части плюс 1 позиция точки (для совместимости с Registry)
	def __len__(self):
		return len(self.__integer) + len(self.__comma) + len(self.__fraction)
	
	# Метод равенства можно реализовать простым способом
	def __eq__(self, other):
		# NEWIT сравнение BigFloat с int и float
		if type(other) is int or type(other) is float:
			# ISSUE пока без проверки знака числа
			other = self.__convert_type(other)
		if self.sign == other.sign:
			return self.integer == other.integer and self.fraction == other.fraction
		return False

	# Неравенство таким же способом не удается реализовать, т.к. требуется выравнивание
	def __lt__(self, other):
		# NEWIT сравнение BigFloat с int и float
		if type(other) is int or type(other) is float:
			other = self.__convert_type(other)
		max_len = self.__max_len(other)
		first = self.extract(*max_len, BigFloat.__STRAIGHT)
		second = other.extract(*max_len, BigFloat.__STRAIGHT)
		# minus = False
		for x, y in zip(first, second):
			if x != y:
				first.close()
				second.close()
			# вывод знака скоординирован в extract
			if x in ['-', '']:
				if x == y:
					minus = True if x else False
				else:
					return x > y
			else:
				if x == y:
					continue
				else:
					return (x < y) ^ minus
		# конец генерации чисел (значит они равны)
		return False

	def __le__(self, other):
		return self == other or self < other

	# NEWIT из-за приведения типов необходимо реализовать все варианты сравнения
	def __gt__(self, other):
		if type(other) is int or type(other) is float:
			other = self.__convert_type(other)
		max_len = self.__max_len(other)
		first = self.extract(*max_len, BigFloat.__STRAIGHT)
		second = other.extract(*max_len, BigFloat.__STRAIGHT)
		# minus = False
		for x, y in zip(first, second):
			if x != y:
				first.close()
				second.close()
			# вывод знака скоординирован в extract
			if x in ['-', '']:
				if x == y:
					minus = True if x else False
				else:
					return x < y
			else:
				if x == y:
					continue
				else:
					return (x > y) ^ minus
		# конец генерации чисел (значит они равны)
		return False

	def __ge__(self, other):
		return self == other or self > other


	# Строковое представление:
	# 1) если ничего не введено, то выводит 0
	# 2) если введено целое число, показывает целое число
	# 3) если введена точка, показывает дробное число
	# 4) если дробной части нет, но есть точка, показывает "х.0" или "0.0"
	def __str__(self):
		# comma = '.' if self.comma else ''
		# NEWIT вывод знака числа
		# sign = '-' if self.__sign else ''
		# integer = '0' if self.comma and not self.__integer else self.__integer
		integer = self.__integer if self.__integer else '0'
		frac = '0' if self.comma and not self.__fraction else self.__fraction
		# если нужен ноль с точкой, можно переделать
		return self.sign + integer + self.comma + frac

	# Для переопределения метода format
	def __format__(self, format_spec):
		return format(str(self), format_spec)

	# генератор сложения (генерирует сбор строки числа)
	# IN: A - объект первого числа
	# IN: B - объект второго числа
	# IN: op - обрабатываемая математическая операция
	# leftside - как обрабатывается операция (меняются ли местами операнды)
	def __operation(self, other, op, leftside: bool = True):
		# Вначале нужно найти максимально длинную часть
		max_len = self.__max_len(other)
		# if op == '-' and self < other:
		# TODO рефакторить после тестов
		if leftside:
			sign = ''
			first = self.extract(*max_len)
			second = other.extract(*max_len)
			# if op == '+' and self.sign: sign = '-'
			if self.sign: sign = '-'
		else:
			# TODO если в '+' число отрицательное, то результат отрицательный
			sign = '-'
			first = other.extract(*max_len)
			second = self.extract(*max_len)
		carry = 0
		# NEWIT зависиомсть формулы расчета от типа операции
		pref = 1 if op == '+' else -1
		# NEWIT имитация знака числа для настройки генератора
		# sign = ''
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
		# NEWIT в конце надо отправить знак числа (для регистра Z)
		yield sign

	def __add__(self, other):
		# NEWIT выбор в зависимости от знака числа
		if self.sign != other.sign:
			# если знаки разные, то это вычитание
			return self.__operation(other, '-', abs(self) >= abs(other))
		# иначе - сложение, знак определяем в __operation
		return self.__operation(other, '+')

	def __sub__(self, other):
		# if self.sign != other.sign:
		# 	return self.__operation(other, '+')
		return self.__operation(other, '-', abs(self) >= abs(other))

	def __abs__(self):
		transition = self
		transition.sign = ''
		return transition


# if __name__ == '__main__':
# 	num0 = BigFloat()
# 	print(str(num0))
# 	print(str(abs(num0)))
