# *****************************************************************************
# МОДУЛЬ:    flags
# ФАЙЛ:      flags.py
# ЗАГОЛОВОК: КЛАСС ФЛАГОВ (ДЛЯ КАЛЬКУЛЯТОРА)
# ОПИСАНИЕ:  Описывает класс флагов калькулятора
# ВЕРСИЯ:    Данный модуль сам создает флаги из переданного описания
# *****************************************************************************

# Импортирование констант
# DEPRECATED 06-06-2020
# from appregistry import CD, CONST, EQ, PI
# Импортирование констант знаков математических операций
from appregistry import MATH_SIGNS
# Импортирование конфигурации флагов
from appregistry import flagsList, eflagsList
class Flags:
	""" КЛАСС ДЛЯ ФЛАГОВ КАЛЬКУЛЯТОРА """

	# Здесь жестко фиксируются атрибуты и методы, которые могут использоваться в классе
	__slots__ = tuple([method for flag in flagsList if flag != 'combs'
						for method in flagsList[flag]['set']] + ['__EFLAGS', '__FLAGS'])

	def __init__(self):
		# стандартные флаги, имеющие значения True\False
		self.__FLAGS = {}
		# расширенные флаги, которые могут иметь разное значение
		self.__EFLAGS = {}
		# заполнить флагами экземпляр Flags
		for flag in flagsList:
			# пропустить комбинированные флаги
			if flag == 'combs': continue
			# создаем стандартные флаги и собираем их в регистр FLAGS
			# инициализируем начальным значением
			self.__FLAGS[flag] = self.__Flag(flag, flagsList[flag]['init'])
			# создать свойства как названия флагов
			setattr(Flags, flag, property(lambda self, f=self.__FLAGS[flag]: f.value))
			# создаем методы изменения флагов (для синонимов)
			for i in range(2):
				# добавление setters с названиями-синонимами
				setattr(Flags, flagsList[flag]['set'][i], lambda self,
						f=self.__FLAGS[flag], v=bool(i): setattr(f, 'value', v))
				# добавление getters с названиями-синонимами как свойств класса,
				# пропуская не установленные свойства (None)
				if flagsList[flag]['get'][i] is not None:
					setattr(Flags, flagsList[flag]['get'][i], property(lambda self,
							f=self.__FLAGS[flag], i=i: (f.value if i else not f.value)))
		# обработка комбинированных флагов (состоящих из двух в данной редакции)
		for flag, props in flagsList['combs'].items():
			setattr(Flags, flag, property(lambda self:
								getattr(self, props[0]) and getattr(self, props[1])))
		# определить сложные флаги
		for eflag, entry in eflagsList.items():
			# создаем флаги и заполняем регистр EFLAGS
			self.__EFLAGS[eflag] = self.__Flag(eflag, entry['init'])
			setattr(Flags, eflag, property(lambda self, f=self.__EFLAGS[eflag]: f.value,
								(lambda self, v, f=self.__EFLAGS[eflag]: setattr(f, 'value', v)
												if v in MATH_SIGNS else self.__mistake(v))))

	def __mistake(self, v):
		raise ValueError(f"invalid operation for calculator: '{v}'")

# ---------------------- Внутренний класс флага ---------------------- #

	class __Flag:

		def __init__(self, name, value):
			self.__name = name
			self.__value = value
			# используется для сохранения начального значения (для очистки clear())
			self.__initvalue = value
		
		@property
		def value(self):
			return self.__value

		@value.setter
		def value(self, val):
			self.__value = val

		# при сбросе к начальным настройкам используется сохраненное значение
		def clear(self):
			self.__value = self.__initvalue

# ----------------------- Комбинации работы ALU ---------------------- #

	# Операция вида B op A ?
	# @property
	# def IS_B_op_A(self):
	# 	return self.IS_EQUAL_PRESSED and self.IS_OPS_CONTINUES

	# # Операция вида A op B ?
	# @property
	# def IS_A_op_B(self):
	# 	return self.IS_EQUAL_PRESSED and self.IS_OPS_STOPPED

	# # Операции продолжаются друг за другом ?
	# @property
	# def IS_NEXT_OPERATION(self):
	# 	return not self.IS_EQUAL_PRESSED and self.IS_OPS_CONTINUES

	# # NEWIT свойство для рефакторинга алгоритма АЛУ
	# @property
	# def IS_UNKNOWN_OPERATION(self):
	# 	return not self.IS_EQUAL_PRESSED and not self.IS_OPS_CONTINUES

# -------------------------------------------------------------------- #
#                                Методы                                #
# -------------------------------------------------------------------- #

	# TODO будет ли работать clear? Создать динамически?
	def clear(self):
		for flag in self.__FLAGS.values():
			flag.clear()
		for eflag in self.__EFLAGS.values():
			eflag.clear()
		# DEPRECATED 06-06-2020 очистка флагов через метод класса Flag
		# self.new_reg_filling()
		# self.disable_ops_continues()
		# self.equal_not_pressed()
		# self.PI = None
