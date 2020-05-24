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

	# ввод цифр
	def test_input_digits(self):
		calc = self.test_initial()
		calc.pressedDigitalKey('5')
		assert "A='5'  (None)  B='0'  EQ=0  CD=0  CONST=0" == calc.displayRegisters()
		calc.pressedDigitalKey('4')
		assert "A='54'  (None)  B='0'  EQ=0  CD=0  CONST=0" == calc.displayRegisters()
		return calc

	# проверка BackSpace BS
	def test_BS(self):
		calc = self.test_input_digits()
		calc.pressedDigitalKey('8')
		assert "A='548'  (None)  B='0'  EQ=0  CD=0  CONST=0" == calc.displayRegisters()
		calc.pressedDigitalKey('\x08')
		assert "A='54'  (None)  B='0'  EQ=0  CD=0  CONST=0" == calc.displayRegisters()
		return calc

	# проверка ввода операции после ввода первого числа
	# ввод второго числа
	def test_input_first_op(self):
		calc = self.test_BS()
		calc.pressedOpcode('+')
		assert "A='54'  (+)  B='54'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('1')
		assert "A='1'  (+)  B='54'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('2')
		assert "A='12'  (+)  B='54'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		return calc

	# нажатие равно
	# @pytest.mark.skip()
	def test_press_equal(self):
		calc = self.test_input_first_op()
		calc.pressedEqual()
		assert "A='66'  (+)  B='12'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# проверка ввода операции после ввода первого числа
	# ввод второго числа, затем продолжающийся ввод операций (и "равно" в конце)
	# @pytest.mark.skip()
	def test_continuos_ops(self):
		calc = self.test_input_first_op()
		calc.pressedOpcode('-')
		assert "A='66'  (-)  B='66'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('1')
		assert "A='1'  (-)  B='66'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('0')
		assert "A='10'  (-)  B='66'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedOpcode('/')
		assert "A='56'  (/)  B='56'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('2')
		assert "A='2'  (/)  B='56'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		# WARNING деление еще не реализовано
		# calc.pressedEqual()
		# assert "A='28.0'  (/)  B='2'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()

	# последовательный ввод "равно" после ввода 2 чисел и одной операции
	# @pytest.mark.skip()
	def test_continuos_equal(self):
		calc = self.test_press_equal()
		calc.pressedEqual()
		assert "A='78'  (+)  B='12'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='90'  (+)  B='12'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='102'  (+)  B='12'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# тест нажатия клавиши ESC "очистка"
	# @pytest.mark.skip()
	def test_escape_clear(self):
		calc = self.test_continuos_equal()
		calc.clear()
		assert "A='0'  (None)  B='0'  EQ=0  CD=1  CONST=0" == calc.displayRegisters()
