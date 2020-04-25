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
		return number

	# добавление цифр, точки
	def test_call(self):
		number = self.test_initial()
		number.integer = '5'
		assert '5' == str(number)
		number.integer = '54'
		assert '54' == str(number)
		number.comma = True
		assert '54.0' == str(number)
		number.fraction = '2'
		assert '54.2' == str(number)
		number.fraction = '27'
		assert '54.27' == str(number)
		return number

	# проверка специального метода сравнения __eq__
	# @pytest.mark.skip()
	def test_equal_method(self):
		number = self.test_call()
		number2 = bigfloat.BigFloat()
		number2.integer = '100'
		number2.comma = True
		number2.fraction = '1'
		assert not (number == number2)
		number3 = bigfloat.BigFloat()
		number3.integer = '100'
		number3.comma = True
		number3.fraction = '1'
		assert number2 == number3
		number2 = bigfloat.BigFloat()
		number2.integer = '100'
		number2.comma = True
		number2.fraction = '1'
		number2.BS()
		number2.BS()
		assert '100' == str(number2)
		number3.BS()
		assert '100.0' == str(number3)
		assert number2 == number3
	
	# проверка специального метода __lt__
	def test_lower_than_method(self):
		number = self.test_call()
		number2 = bigfloat.BigFloat()
		number2.integer = '100'
		number2.comma = True
		number2.fraction = '1'
		assert number < number2

	# проверка специального метода __le__
	def test_lower_than__equal_method(self):
		number = self.test_call()
		number2 = bigfloat.BigFloat()
		number2.integer = '100'
		number2.comma = True
		number2.fraction = '1'
		assert number <= number2
		number3 = bigfloat.BigFloat()
		number3.integer = '100'
		number3.comma = True
		number3.fraction = '1'
		# num2 и num3 равны
		assert number2 <= number3
		assert number2 >= number3
		# num3 больше num
		assert number3 >= number

	# сравнение равенства BigFloat с числами типов int и float
	def test_equal_with_number_method(self):
		number = self.test_call()
		assert number == 54.27
		assert not (number == 100)
		number.integer = '100'
		number.fraction = ''
		number.comma = False
		assert number == 100
		assert number == 100.0
		number.integer = ''
		assert number == 0
		assert number == 0.0
		number.comma = True
		assert number == 0
		assert number == 0.0

	# сравнение неравенства BigFloat с числами типов int и float
	def test_lower_than_equal_with_number_method(self):
		number = self.test_call()
		# сравнение с числом number == 54.27
		assert number <= 55
		assert number < 55
		assert number <= 55.0
		assert number < 55.0
		assert number <= 54.28
		assert number < 54.28
		assert number >= 54
		assert number > 54
		assert number > 54.26
		assert number >= 54.26
		assert number > 54.0
		assert number >= 54.0
		assert number > 0
		assert number > 0.0
		assert number >= 0
		assert number >= 0.0
