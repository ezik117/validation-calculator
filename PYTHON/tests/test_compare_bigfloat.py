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
		number.comma = '.'
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
		number2.comma = '.'
		number2.fraction = '1'
		assert not (number == number2)
		number3 = bigfloat.BigFloat()
		number3.integer = '100'
		number3.comma = '.'
		number3.fraction = '1'
		assert number2 == number3
		number2 = bigfloat.BigFloat()
		number2.integer = '100'
		number2.comma = '.'
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
		number2.comma = '.'
		number2.fraction = '1'
		assert number < number2

	# проверка специального метода __le__
	# @pytest.mark.skip()
	def test_lower_than_equal_method(self):
		number = self.test_call()
		number2 = bigfloat.BigFloat()
		number2.integer = '100'
		number2.comma = '.'
		number2.fraction = '1'
		assert number <= number2
		number3 = bigfloat.BigFloat()
		number3.integer = '100'
		number3.comma = '.'
		number3.fraction = '1'
		# num2 и num3 равны
		assert number2 == number3
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
		number.comma = ''
		assert number == 100
		assert number == 100.0
		number.integer = ''
		assert number == 0
		assert number == 0.0
		number.comma = '.'
		assert number == 0
		assert number == 0.0

	# сравнение неравенства BigFloat с числами типов int и float
	# @pytest.mark.skip()
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

	# тест сравнения отрицательных чисел
	# @pytest.mark.skip()
	def test_equal_negative_number(self):
		number = self.test_call()
		# number == -54.27
		number.sign = '-'
		# number2 == 100.1
		number2 = bigfloat.BigFloat()
		number2.integer = '100'
		number2.comma = '.'
		number2.fraction = '1'
		assert not (number == number2)
		assert number < number2
		assert number <= number2
		# number2 == -100.1
		number2.sign = '-'
		assert not (number == number2)
		assert number > number2
		assert number >= number2
		# number = -100.1
		number.integer = '100'
		number.fraction = '1'
		assert number == number2
		# number = 0
		number.integer = ''
		number.fraction = ''
		number.comma = ''
		number.sign = ''
		assert number > number2
		assert number >= number2

	# сравнение неравенства BigFloat с числами типов int и float
	# @pytest.mark.skip()
	def test_lower_than_equal_with_negative_number_method(self):
		number = self.test_call()
		# сравнение с числом number == -54.27
		number.sign = '-'
		assert number >= -55
		assert number > -55
		assert number >= -55.0
		assert number > -55.0
		assert number >= -54.28
		assert number > -54.28
		assert number <= -54
		assert number < -54
		assert number < -54.26
		assert number <= -54.26
		assert number < -54.0
		assert number <= -54.0
		assert number < 0
		assert number < 0.0
		assert number <= 0
		assert number <= 0.0

	# проверка специального метода сравнения __eq__ с учетом знака
	# @pytest.mark.skip()
	def test_equal_method(self):
		number = self.test_call()
		number.sign = '-'
		number2 = bigfloat.BigFloat()
		number2.integer = '54'
		number2.comma = '.'
		number2.fraction = '27'
		number2.sign = '-'
		assert number == number2
		assert number == -54.27
		assert number2 == -54.27
