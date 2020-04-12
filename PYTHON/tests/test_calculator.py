import pytest
import sys

sys.path.append('..')
from .. import calculator

class TestFlags():

# WARNING Изменение флага EQ невозможно протестировать, т.к. он изменяется
# в методе pressedDigitalKey(), который из-за особенностей реализации
# невозможно контролировать. Его действия эмулируются тестовым классом

# ------------------------- Тестовые функции ------------------------- #

	# инициализация калькулятора
	def test_initial(self):
		calc = calculator.Calculator(3)
		# calc = self.__initial()
		assert "A='0'  (None)  B='0'  EQ=0  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# ввод цифр
	def test_input_digits(self):
		calc = self.test_initial()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('5')
		assert "A='5'  (None)  B='0'  EQ=0  CD=0  CONST=0" == calc.displayRegisters()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('4')
		assert "A='54'  (None)  B='0'  EQ=0  CD=0  CONST=0" == calc.displayRegisters()
		return calc

	# проверка BackSpace BS
	def test_BS(self):
		calc = self.test_input_digits()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('8')
		assert "A='548'  (None)  B='0'  EQ=0  CD=0  CONST=0" == calc.displayRegisters()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('\x08')
		assert "A='54'  (None)  B='0'  EQ=0  CD=0  CONST=0" == calc.displayRegisters()
		return calc

	# проверка ввода операции после ввода первого числа
	# ввод второго числа
	def test_input_first_op(self):
		calc = self.test_BS()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedOpcode('+')
		assert "A='54'  (+)  B='54'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('1')
		assert "A='1'  (+)  B='54'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('2')
		assert "A='12'  (+)  B='54'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		return calc
		# calc.flags.EQ = True
		# calc.pressedEqual()
		# assert "A='54'  (+)  B='66.0'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()

	# нажатие равно
	def test_press_equal(self):
		calc = self.test_input_first_op()
		calc.flags.EQUAL_PRESSED
		calc.pressedEqual()
		assert "A='54'  (+)  B='66.0'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# проверка ввода операции после ввода первого числа
	# ввод второго числа, затем продолжающийся ввод операций (и "равно" в конце)
	def test_continuos_ops(self):
		calc = self.test_input_first_op()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedOpcode('-')
		assert "A='66.0'  (-)  B='66.0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('1')
		assert "A='1'  (-)  B='66.0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('0')
		assert "A='10'  (-)  B='66.0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedOpcode('/')
		assert "A='56.0'  (/)  B='56.0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.flags.EQUAL_NOT_PRESSED
		calc.pressedDigitalKey('2')
		assert "A='2'  (/)  B='56.0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.flags.EQUAL_PRESSED
		calc.pressedEqual()
		assert "A='56.0'  (/)  B='28.0'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()

	# последовательный ввод "равно" после ввода 2 чисел и одной операции
	def test_continuos_equal(self):
		calc = self.test_press_equal()
		calc.flags.EQUAL_PRESSED
		calc.pressedEqual()
		assert "A='120.0'  (+)  B='66.0'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		calc.flags.EQUAL_PRESSED
		calc.pressedEqual()
		assert "A='186.0'  (+)  B='66.0'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		calc.flags.EQUAL_PRESSED
		calc.pressedEqual()
		assert "A='252.0'  (+)  B='66.0'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# тест нажатия клавиши ESC "очистка"
	def test_escape_clear(self):
		calc = self.test_continuos_equal()
		calc.clear()
		assert "A='0'  (None)  B='0'  EQ=0  CD=1  CONST=0" == calc.displayRegisters()