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

class Registry:
	""" КЛАСС ДЛЯ РЕГИСТРА КАЛЬКУЛЯТОРА """
	# конструктор
	# IN: name - буква регистра, необходима для избежания получения одинаковой ссылки на
	#            разные объекты
	# IN: base - ссылка на базовый класс калькулятора для 
	def __init__(self, name: str):
		# NEWIT закрыть изменение имени регистра извне
		self.__name = name  # буква регистра
		# NEWIT закрыть изменение значения регистра извне напрямую (кроме регистра Z)
		self._value = '0'  # значение регистра как строка
		# NEWIT флаг ввода точки
		self._comma = False # событие ввода точки
		# Длины каждой части
		self.__len_int = 0
		self.__len_frac = 0

# -------------------------- Свойства класса ------------------------- #

	# NEWIT getter значения регистра
	@property
	def value(self):
		return self._value

	# NEWIT setter регистра Z
	@value.setter
	def value(self, value):
		if self.__name == 'Z':
			self._value = value
		else:
			raise ValueError("Registry: unable to set value for registry '{}'".format(self.__name))

	# TODO можно удалить в будущем (для тестов)
	@property
	def comma(self):
		return int(self._comma)

	@comma.setter
	def comma(self, value):
		if self.__name == 'Z':
			self._comma = value
		else:
			raise ValueError("Registry: unable to set value for registry '{}'".format(self.__name))

	# NEWIT Длины частей
	@property
	def len_int(self):
		return self.__len_int

	@property
	def len_frac(self):
		return self.__len_frac

# --------------------------- Методы класса -------------------------- #

	# сброс содержимого регистра
	def clear(self):
		self._value = '0'
		# NEWIT сброс флага запятой при очистке
		self._comma = False
		self.__len_int = 0
		self.__len_frac = 0

	# затереть один символ с конца
	def BS(self):
		if len(self._value) > 1:
			# NEWIT сброс флага запятой, если она затерта
			if self._value[-1] == '.':
				self._comma = False
			self._value = self._value[:-1]
		else:
			self._value = '0'

	# ввести один символ в конец
	# IN: c - цифра или точка в строковом представлении
	# IN: newInput - если True, то содержимое регистра заменяется новым значением в 'c'
	#              - если False, то значение в 'c' добавляется в конец значения регистра
	def input(self, c: str, flags: object):
		# NEWIT Если новый ввод, то сброс флага запятой
		if flags.IS_NEW_INPUT: self._comma = False
		# NEWIT защита от ввода второй запятой
		# if c == '.' and flags.IS_REG_FILLING and '.' in self._value:
		if c == '.' and flags.IS_REG_FILLING and self._comma:
			raise ValueError("could not convert string to float: '{0}'".format(self._value + c))
		# NEWIT поднятие флага запятой, если введена запятая
		if c == '.': self._comma = True
		if (len(self._value) == 1 and self._value == "0") or flags.IS_NEW_INPUT:
			self._value = c
		else:
			self._value += c

	# копирует значение из другого регистра класса Registry
	def copyFrom(self, R:'Registry'):
		self._value = R.value
		# NEWIT копирование флага запятой
		self._comma = R._comma
		# TODO нужно будет копировать длины частей
		self.__len_int = R.__len_int
		self.__len_frac = R.__len_frac

	# NEWIT Работа метода:
	# 1) удаление незначащих нулей дробной части
	# 2) определение длин целой и дробной частей
	# TODO не протестировано в pytest
	def prepare(self):
		if self._comma:
			self._value = self._value.rstrip('0')
			if self._value.endswith('.'):
				self._value += '0'
			self.__len_int = self._value.find('.')
			self.__len_frac = len(self._value) - self.__len_int - 1
		else:
			self.__len_int = len(self._value)
			# TODO тест ответа всегда с запятой
			# self.__len_frac = 0
			self.__len_frac = 1
			self._value += '.0'
			self._comma = True
		# print(self.__len_int, self.__len_frac)

	# NEWIT Генератор, извлекающий по 1 цифре из строки числа,
	# скорректированный на длину максимального числа
	# IN: max_int - максимальная длина целой части числа из двух
	# IN: max_frac - максимальная длина дробной части числа из двух
	def extract(self, max_int: int=0, max_frac: int=0):
		# Начинаем с конца
		# 1) коррекция дробной части (len_frac либо равна, либо меньше max_frac)
		for _ in range(max_frac - self.__len_frac):
			yield 0
		# 2) генерирование дробной части, затем целой, пропуская точку (с конца)
		for idx in range(len(self._value)-1, -1, -1):
			if idx > self.__len_int:
				yield int(self._value[idx])
			elif idx == self.__len_int:
				yield None
			else:
				yield int(self._value[idx])
		# 3) коррекция целой части (аналогично дробной (1))
		for _ in range(max_int - self.__len_int):
			yield 0

# ------------------------ Специальные методы ------------------------ #

	# TODO переделать, когда будут дробные числа
	def __str__(self):
		return self._value


class RegistryZ(Registry):

	# Конструктор для открытия файла логов
	def __init__(self, value):
		super().__init__(value)
		self.fh = open('input_z.log', 'w', encoding='utf8')

	def input(self, c: str, flags: object, A, B, op):
		if c == 'new':
			print('Начало сложения (add)', file=self.fh)
			return
		# NEWIT Если новый ввод, то сброс флага запятой
		# if flags.IS_NEW_INPUT:
		# 	self._comma = False
		# NEWIT защита от ввода второй запятой
		# if c == '.' and flags.IS_REG_FILLING and '.' in self._value:
		if c == '.' and flags.IS_REG_FILLING and self._comma:
			raise ValueError("could not convert string to float: '{0}'".format(self._value + c))
		# NEWIT поднятие флага запятой, если введена запятая
		if c == '.':
			self._comma = True
		# if (len(self._value) == 1 and self._value == "0") or flags.IS_NEW_INPUT:
		# 	self._value = c
		# else:
		self._value = c + self._value
		print(f"A='{A}'  ({op})  B='{B}'  Z='{self}'"
				f"  CommaZ={self._comma}  CommaA={A.comma}"
				f"  EQ={int(flags.EQ)}  CD={int(flags.CD)}  CONST={int(flags.CONST)}", file=self.fh)
