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

	# ввод положительного числа
	def test_input_positive(self):
		number = self.test_initial()
		number.integer = '54'
		number.comma = '.'
		number.fraction = '27'
		assert '54.27' == str(number)
		return number

	# ввод отрицательного числа
	def test_input_negative(self):
		number = self.test_input_positive()
		number.sign = '-'
		assert '-54.27' == str(number)
		return number

	# тест abs с положительным числом
	def test_abs_positive(self):
		number = self.test_input_positive()
		assert '54.27' == str(abs(number))

	# тест abs с положительным числом
	def test_abs_positive(self):
		number = self.test_input_negative()
		assert '54.27' == str(abs(number))

	# тест сравнения модулей числа
	def test_abs_with_abs(self):
		number = self.test_input_positive()
		number2 = self.test_input_negative()
		assert number != number2
		assert abs(number) == abs(number2)

	# тест сравнения abs  с нулем
	def test_abs_with_zero(self):
		number = self.test_input_positive()
		number0 = bigfloat.BigFloat()
		assert number > number0
		assert number >= number0
		assert abs(number) > abs(number0)
		assert abs(number) >= abs(number0)

	# тест сравнения abs  с нулем
	def test_abs_with_zero(self):
		number = self.test_input_negative()
		number0 = bigfloat.BigFloat()
		assert number < number0
		assert number <= number0
		assert abs(number) > abs(number0)
		assert abs(number) >= abs(number0)
