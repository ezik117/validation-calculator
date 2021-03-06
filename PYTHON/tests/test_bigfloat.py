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

	# затереть последние смиволы
	# @pytest.mark.skip()
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
	@pytest.mark.skip()
	def test_first_point(self):
		number = self.test_initial()
		number('.')
		assert '0.0' == str(number)
		number('2')
		assert '0.2' == str(number)
		number('7')
		assert '0.27' == str(number)

	# проверка ввода первых нулей
	@pytest.mark.skip()
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
	# @pytest.mark.skip()
	def test_lower_than_method(self):
		number = self.test_call()
		number2 = bigfloat.BigFloat()
		number2.integer = '100'
		number2.comma = '.'
		number2.fraction = '1'
		assert number < number2

	# проверка специального метода __le__
	# @pytest.mark.skip()
	def test_lower_than__equal_method(self):
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
		assert number2 <= number3
		assert number2 >= number3
		# num3 больше num
		assert number3 >= number
