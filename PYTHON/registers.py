# *****************************************************************************
# МОДУЛЬ:    GMP-CALCULATOR
# ФАЙЛ:      REGISTERS.PY
# ЗАГОЛОВОК: КЛАССЫ РЕГИСТРОВ
# ОПИСАНИЕ:  Описывает класс регистров калькулятора
# *****************************************************************************

# FIXME ТЗ устарело
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
# - [x] добавить свойства получения длин каждой части (необходимо для дальнейших расчетов)
# - [x] исправить метод input() для возможности ввода дробных величин
# - [x] ограничение ввода незначащих нулей для дробной части
# ------------
# Реализация 2:
# 1) Узнать длину каждой части через find ?
# 2) Запомнить их в свойствах

import bigfloat as bf

class Registry:
	""" КЛАСС ДЛЯ РЕГИСТРА КАЛЬКУЛЯТОРА """
	# конструктор
	# IN: name - буква регистра, необходима для избежания получения одинаковой ссылки на
	#            разные объекты
	def __init__(self, name: str):
		self.__name = name  # буква регистра
		# TODO Можно закрыть изменение извне, если реализовать свойства в класса регистра Z ???
		self._value = bf.BigFloat()  # значение регистра как объект числа BigFloat
		# NEWIT не нужны comma, len_int, len_frac

# -------------------------- Свойства класса ------------------------- #

	# getter значения регистра
	# NEWIT переведен на объект числа
	@property
	def value(self):
		return self._value

	# KILLME можно удалить после реализации все операций
	@value.setter
	def value(self, value):
		raise ValueError("Registry: unable to set value for registry '{}'".format(self.__name))

	# TODO свойство используется для вывода результатов (если не нужно, удалить)
	# NEWIT переведен на объект числа
	@property
	def comma(self):
		return self._value.comma

	# NEWIT Длины частей (используются в АЛУ). Переведены на объект числа
	@property
	def len_int(self):
		return self._value.len_int

	@property
	def len_frac(self):
		return self._value.len_frac

	@property
	def name(self):
		return self.__name

	@property
	def sign(self):
		return self._value.sign
# --------------------------- Методы класса -------------------------- #

	# сброс содержимого регистра
	def clear(self):
		# NEWIT просто создаем новый пустой объект
		self._value = bf.BigFloat()
		# NEWIT т.к. все контролируется объектом числа, удаляем comma, len_int, len_frac

	# затереть один символ с конца
	def BS(self):
		# NEWIT затирание отдаем в объект числа
		self._value.BS()

	# ввести один символ в конец
	# IN: c - цифра или точка в строковом представлении
	# IN: newInput - если True, то содержимое регистра заменяется новым значением в 'c'
	#              - если False, то значение в 'c' добавляется в конец значения регистра
	def input(self, c: str, flags: object):
		# NEWIT запятой заведует объект числа
		# NEWIT если новый ввод, создаем новый объект числа
		if flags.IS_NEW_INPUT:
			self._value = bf.BigFloat()
		# if c == '.' and self._value.comma:
		# 	raise ValueError("could not convert string to float: '{0}{1}'".format(self._value, c))
		if c == '.':
			# Ошибка при вводе второй точки
			if self._value.comma:
				raise ValueError("could not convert string to float: '{0}{1}'".format(self._value, c))
			else:
				self._value.comma = c
		elif self._value.comma:
			self._value.fraction += c
		# в том числе отсекает ввод незанчащих 0 целой части
		# TODO ??? заменить self.__integer на len == 0
		elif self._value.integer or c != '0':
			self._value.integer += c


	# копирует значение из другого регистра класса Registry
	def copyFrom(self, R:'Registry'):
		# WARNING передается ссылка на объект; это то, что нужно ?
		self._value = R.value.copy()
		# NEWIT Теперь не нужно их копировать comma, len_int, len_frac

	# NEWIT prepare опять нужен, делегируется объекту числа
	def truncate(self):
		self._value.truncate()

	# IN: max_int - максимальная длина целой части числа из двух
	# IN: max_frac - максимальная длина дробной части числа из двух
	# WARNING не используется?
	# def extract(self, max_int: int=0, max_frac: int=0):
		# NEWIT пока используем ссылку на extract из BigFloat
		# return self._value.extract(max_int, max_frac)

# ------------------------ Специальные методы ------------------------ #

	def __str__(self):
		return str(self._value)


class RegistryZ(Registry):

	# Конструктор для открытия файла логов
	def __init__(self):
		super().__init__('Z')
		# логгирование сборки числа в регистре Z
		# self.fh = open('PYTHON/logs/input_z.log', 'w', encoding='utf8')
		# из тестов pytest
		# self.fh = open('input_z.log', 'w', encoding='utf8')

	# NEWIT свойство значения
	@property
	def value(self):
		return super().value
	
	@value.setter
	def value(self, merger):
		# self._value = val

	# def input(self, c: str, flags: object, A, B, op):
	# def input(self, c: str, flags: object):
		for c in merger:
			# if c == '.' and self._value.comma:
			# 	raise ValueError("could not convert string to float: '{0}{1}'".format(self._value, c))
			if c == '-' or c == '':
				self._value.sign._sign = c
			elif c == '.':
				if self._value.comma:
					raise ValueError("could not convert string to float: '{0}{1}'".format(self._value, c))
				else:
					self._value.comma = c
					# NEWIT но, если приходит запятая, то значит собирали дробную часть,
					# меняем местами и начинаем собирать настоящую целую часть
					# TODO можно обрезать незначащие нули справа в дробной части
					self._value.fraction = self._value.integer
					self._value.integer = ''
			# elif self._value.comma:
			# NEWIT вначале собираем все в целое число
			else:
				self._value.integer = c + self._value.integer
			# в том числе отсекает ввод незанчащих 0 целой части
			# TODO ??? заменить self.__integer на len == 0
			# elif self._value.fraction or c != 0:
			# 	self._value.fraction = c + self._value.fraction

		# print(f"A='{A}'  ({op})  B='{B}'  Z='{self}'"
		# 		f"  CommaZ={self._value.comma}  CommaA={A.value.comma}"
		# 		f"  Zint={self._value.integer}  Zfrac={self._value.fraction}"
		# 		f"  EQ={int(flags.EQ)}  CD={int(flags.CD)}  CONST={int(flags.CONST)}", file=self.fh)
