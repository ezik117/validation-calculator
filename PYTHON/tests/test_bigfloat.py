# *****************************************************************************
# МОДУЛЬ:    test_bigfloat
# ФАЙЛ:      test_bigfloat.py
# ЗАГОЛОВОК: КЛАСС тестов для больших чисел
# ОПИСАНИЕ:  Класс служит для тестирования через pytest класса BogFloat
# *****************************************************************************

import pytest
import sys

sys.path.append('..')
from .. import bigfloat

class TestBigFloat():

	# ------------------------- Тестовые функции ------------------------- #

	# инициализация числа
	def test_initial(self):
		number = bigfloat.BigFloat()
		assert '0' == str(number)
		# assert "A='0'  (None)  B='0'  EQ=0  CD=1  CONST=0" == calc.displayRegisters()
		return number

	# добавление цифр, точки
	def test_call(self):
		number = self.test_initial()
		number('5')
		assert '5' == str(number)
		number('4')
		assert '54' == str(number)
		number('.')
		assert '54.0' == str(number)
		number('2')
		assert '54.2' == str(number)
		number('7')
		assert '54.27' == str(number)
		return number

	# затереть последние смиволы
	def test_backspace(self):
		number = self.test_call()
		number.BS()
		assert '54.2' == str(number)
		number.BS()
		assert '54.0' == str(number)
		number.BS()
		assert '54' == str(number)
		number.BS()
		assert '5' == str(number)
		number.BS()
		assert '0' == str(number)
		number.BS()
		assert '0' == str(number)
		return number

	# проверить на первую точку
	def test_first_point(self):
		number = self.test_initial()
		number('.')
		assert '0.0' == str(number)
		number('2')
		assert '0.2' == str(number)
		number('7')
		assert '0.27' == str(number)

	# проверка ввода первых нулей
	def test_first_zero(self):
		number = self.test_initial()
		number('0')
		assert '0' == str(number)
		number('0')
		assert '0' == str(number)
		number('.')
		assert '0.0' == str(number)
		number.BS()
		assert '0' == str(number)