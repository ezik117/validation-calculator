# *****************************************************************************
# МОДУЛЬ:    test_calculator
# ФАЙЛ:      test_calculator.py
# ЗАГОЛОВОК: КЛАСС тестов для калькулятора
# ОПИСАНИЕ:  Класс служит для тестирования через pytest калькулятора Calculator
# *****************************************************************************

import pytest
import sys

sys.path.append('..')
from .. import calculator

class TestFlags():

# ------------------------- Тестовые функции ------------------------- #

	# инициализация калькулятора
	def test_initial(self):
		calc = calculator.Calculator(3)
		assert "A='0'  (None)  B='0'  EQ=0  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# ввод отрицательного числа
	def test_input_negative_number(self):
		calc = self.test_initial()
		calc.pressedOpcode('-')
		assert "A='0'  (-)  B='0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('5')
		calc.pressedDigitalKey('4')
		assert "A='54'  (-)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('.')
		assert "A='54.0'  (-)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('4')
		assert "A='54.4'  (-)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedOpcode('+')
		assert "A='-54.4'  (+)  B='-54.4'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		return calc

	# сложение первого отрицательного числа и второго положительного
	# ввод второго положительного числа
	# @pytest.mark.skip()
	def test_input_first_op(self):
		calc = self.test_input_negative_number()
		calc.pressedDigitalKey('1')
		calc.pressedDigitalKey('2')
		assert "A='12'  (+)  B='-54.4'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('1')
		assert "A='12.1'  (+)  B='-54.4'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		return calc

	# нажатие равно (сложение положительного и отрицательного чисел)
	# @pytest.mark.skip()
	def test_press_equal(self):
		calc = self.test_input_first_op()
		calc.pressedEqual()
		assert "A='-42.3'  (+)  B='12.1'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# сложение получившегося отрицательного числа с новым положительным числом
	# ввод второго числа, затем продолжающийся ввод операций (и "равно" в конце)
	# @pytest.mark.skip()
	def test_continuos_ops(self):
		calc = self.test_input_first_op()
		calc.pressedOpcode('+')
		assert "A='-42.3'  (+)  B='-42.3'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('1')
		assert "A='1'  (+)  B='-42.3'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('0')
		assert "A='10'  (+)  B='-42.3'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		# Дроби портятся пока нереализованной операцией "-"
		calc.pressedOpcode('+')
		assert ("A='-32.3'  (+)  B='-32.3'  EQ=0  CD=1  CONST=1") == calc.displayRegisters()
		calc.pressedDigitalKey('2')
		assert ("A='2'  (+)  B='-32.3'  EQ=0  CD=0  CONST=1") == calc.displayRegisters()
		calc.pressedEqual()
		assert ("A='-30.3'  (+)  B='2'  EQ=1  CD=1  CONST=0") == calc.displayRegisters()

	# последовательный ввод "равно" (прибавка полижительного к отрицательному)
	# @pytest.mark.skip()
	def test_continuos_equal(self):
		calc = self.test_press_equal()
		calc.pressedEqual()
		assert "A='-30.2'  (+)  B='12.1'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='-18.1'  (+)  B='12.1'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='-6.0'  (+)  B='12.1'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='6.1'  (+)  B='12.1'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# тест нажатия клавиши ESC "очистка"
	# @pytest.mark.skip()
	def test_escape_clear(self):
		calc = self.test_continuos_equal()
		calc.clear()
		assert "A='0'  (None)  B='0'  EQ=0  CD=1  CONST=0" == calc.displayRegisters()
		# WARNING нет проверки очистки запятой
		return calc

	# операция вида (-B) - (-A)
	def test_input_negative_second_number(self):
		calc = self.test_initial()
		calc.pressedOpcode('-')
		assert "A='0'  (-)  B='0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('5')
		calc.pressedDigitalKey('4')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('4')
		assert "A='54.4'  (-)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedOpcode('-')
		assert "A='-54.4'  (-)  B='-54.4'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		# второе число
		calc.pressedDigitalKey('1')
		calc.pressedDigitalKey('2')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('1')
		assert "A='12.1'  (-)  B='-54.4'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='-66.5'  (-)  B='12.1'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc
