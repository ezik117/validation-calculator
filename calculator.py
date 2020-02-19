# *****************************************************************************
# МОДУЛЬ:    CALCULATOR.PY
# ФАЙЛ:      CALCULATOR.PY
# ЗАГОЛОВОК: КЛАССЫ КАЛЬКУЛЯТОРА ПОВЫШЕННОЙ ТОЧНОСТИ
# ОПИСАНИЕ:  Содержит реализацию основных математических операций на языке
#            Python (сложение, вычитание, умножение, деление).
#            Операции выполнены с использованием хранения чисел в строках и
#            алгоритм выполнен таким образом что можно задать высокую точность
#            десятичной дроби (более 15 чем у стандарного double). Точность
#            ограничивается только максимально возможной длиной строки (для 
#            Python x64 это 64Гб памяти (размер строки зависит от типа кодировки))
#            Числа хранятся в обычной записи (т.е. без использования мантиссы)
# *****************************************************************************

# ================================================================================================

class Registry:
	"""КЛАСС ДЛЯ ХРАНЕНИЯ ЧИСЛА (РЕГИСТР)"""

	# конструктор
	def __init__(self):
		# --- свойства -------
		self._positive = True   # знак числа
		self._integer = []      # целая часть числа, как список байтов от 0 до 9
		self._fractional = []   # дробная часть числа, как список байтов от 0 до 9

	# сброс значения регистра
	def reset(self):
		self._positive = True
		self._integer = []
		self._fractional = []

	# загрузка числа в регистр
	# IN: number - строка вида "-1235.56", "7", "12,5", "5.", ".6"
	# OUT: True - если загрузка удачная, False - если парсинг не удался
	def load(self:object, number:str):
		# проверка ввода
		try:
			number = number.replace(",", ".") # если допустить что дробная часть через точку строго, то убрать для скорости
			temp = float(number)
		except:
			return False # ошибка загрузки
		
		# сброс регистра
		self.reset()
		
		# загрузка знака, целой и дробной части
		currentPart = self._integer
		for n in number:
			if n.isdigit(): # число - заносим в текущую часть регистра
				currentPart.append(int(n))
			else:              
				if (n == '-'): # проверка на знак
					self._positive = False
				elif (n == '.'): # переключение на дробную часть
					currentPart = self._fractional
				else:
					return False # какая то хрень попалась
		return True
				
	# выравнивает целую или дробную части с заданным количеством цифр в ней,
	# если size больше чем текущая длина. Добавляет нули впереди для целой части
	# и нули в конце для дробной
	# IN: part- принимает одно из значений "_integer" или "_fractional"
	# IN: size - длина числа для выравнивания
	# OUT: False если ошибка, True - выровнено
	def align(self:object, part:str, size:int):
		try:
			t = getattr(self, part)
			if (len(t) < size):
				if part == "_integer":
					t = [0 for x in range(size - len(t))] + t
				elif part == "_fractional":
					t = t + [0 for x in range(size - len(t))]
				else:
					return False
				setattr(self, part, t)
		except:
			return False
		
		return True
		
	# возвращает строку значения регистра
	# в качестве разделителя целой и дробной части используется точка
	# так же удаляются первые и последние нули
	# IN: raw - если True, строка формируется с дополенными нулями, как есть
	#         - если не указано, то усекаются лидирующие и завершающие нули
	def buildString(self, raw=False):
		sign = ("" if self._positive else "-")
		numInt = ("".join(map(str,self._integer)) if raw else ("".join(map(str,self._integer))).lstrip("0"))
		numFrac = ("".join(map(str, self._fractional)) if raw else ("".join(map(str, self._fractional))).rstrip("0"))
		
		return sign + (numInt if len(numInt) > 0 else "0") + ("." + numFrac if len(numFrac)> 0 else "")


# ================================================================================================

class Calc:
	"""ОСНОВНОЙ КЛАСС КАЛЬКУЛЯТОРА"""
	# --- публичные методы --------------------------------

	# конструктор
	def __init__ (self:object):
		# публичные свойства (аттрибуты)
		self.A = Registry() # регистр A
		self.B = Registry() # регистр B
		# приватные свойства
		self.__STACK = []     # стек

	# сложение
	# IN: A - первое значение для сложения, если не указано берется текущее значение из регистра A
	# IN: B - второе значение для сложения, если не указано берется текущее значение из регистра B
	# OUT: результат помещается в регистр A, регистр B не уничтожается
	def add(self:object, B:str=None, A:str=None):
		# загрузка чисел
		if B:
			self.B.load(B)
		if A:
			self.A.load(A)

		# логика сложения здесь, пока показывает загруженные числа
		print("A=" + self.A.buildString(raw=True))
		print("B=" + self.B.buildString(raw=True))

	# вычитание
	def sub(self:object):
		pass

	# умножение
	def mul(self:object):
		pass

	# деление
	def div(self:object):
		pass

	# --- приватные методы --------------------------------

	# положить данные в стек
	def __stackPush(self:object, data:object):
		self.__STACK.append(getattr(self, regisry))

	# достать данные из стека
	def __stackPop(self:object):
		if len(self.__STACK) > 0:
			return self.__STACK.pop()
		else:
			return None

	# очистить стек
	def __stackClear(self:object):
		self.__STACK = []