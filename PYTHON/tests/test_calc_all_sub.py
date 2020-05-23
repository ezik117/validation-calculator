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

class TestSub():

# ------------------------- Тестовые функции ------------------------- #

	# инициализация калькулятора
	def test_initial(self):
		calc = calculator.Calculator(3)
		assert "A='0'  (None)  B='0'  EQ=0  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# операция вида (big +B) - (small +A)
	def test_positive_bigB_sub_positive_smallA(self):
		calc = self.test_initial()
		calc.pressedOpcode('+')
		assert "A='0'  (+)  B='0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('5')
		calc.pressedDigitalKey('4')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('4')
		assert "A='54.4'  (+)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedOpcode('-')
		assert "A='54.4'  (-)  B='54.4'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		# второе число
		calc.pressedDigitalKey('1')
		calc.pressedDigitalKey('2')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('1')
		assert "A='12.1'  (-)  B='54.4'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='42.3'  (-)  B='12.1'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# операция вида (small +B) - (big +A)
	def test_positive_smallB_sub_positive_bigA(self):
		calc = self.test_initial()
		calc.pressedOpcode('+')
		assert "A='0'  (+)  B='0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('1')
		calc.pressedDigitalKey('2')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('5')
		assert "A='12.5'  (+)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedOpcode('-')
		assert "A='12.5'  (-)  B='12.5'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		# второе число
		calc.pressedDigitalKey('5')
		calc.pressedDigitalKey('8')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('7')
		assert "A='58.7'  (-)  B='12.5'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='-46.2'  (-)  B='58.7'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# операция вида (equal +B) - (equal +A)
	def test_positive_smallB_sub_equal_positive_bigA(self):
		calc = self.test_initial()
		calc.pressedOpcode('+')
		assert "A='0'  (+)  B='0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('1')
		calc.pressedDigitalKey('2')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('5')
		assert "A='12.5'  (+)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedOpcode('-')
		assert "A='12.5'  (-)  B='12.5'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		# второе число
		calc.pressedDigitalKey('1')
		calc.pressedDigitalKey('2')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('5')
		assert "A='12.5'  (-)  B='12.5'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='0.0'  (-)  B='12.5'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
		return calc

	# операция вида (equal -B) - (equal -A)
	def test_negative_bigB_sub_equal_negative_smallA(self):
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
		calc.pressedEqual()
		# FIXME баг операции
		assert "A='0.0'  (-)  B='-54.4'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()

	# операция вида (big -B) - (small +A)
	def test_negative_bigB_sub_positive_smallA(self):
		calc = self.test_initial()
		calc.pressedOpcode('-')
		assert "A='0'  (-)  B='0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('5')
		calc.pressedDigitalKey('4')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('4')
		assert "A='54.4'  (-)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedOpcode('+')
		assert "A='-54.4'  (+)  B='-54.4'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('1')
		calc.pressedDigitalKey('2')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('5')
		assert "A='12.5'  (+)  B='-54.4'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='-41.9'  (+)  B='12.5'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()

	# операция вида (small -B) - (big +A)
	def test_negative_smallB_sub_positive_bigA(self):
		calc = self.test_initial()
		calc.pressedOpcode('-')
		assert "A='0'  (-)  B='0'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('1')
		calc.pressedDigitalKey('2')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('5')
		assert "A='12.5'  (-)  B='0'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedOpcode('+')
		assert "A='-12.5'  (+)  B='-12.5'  EQ=0  CD=1  CONST=1" == calc.displayRegisters()
		calc.pressedDigitalKey('5')
		calc.pressedDigitalKey('4')
		calc.pressedDigitalKey('.')
		calc.pressedDigitalKey('8')
		assert "A='54.8'  (+)  B='-12.5'  EQ=0  CD=0  CONST=1" == calc.displayRegisters()
		calc.pressedEqual()
		assert "A='42.3'  (+)  B='54.8'  EQ=1  CD=1  CONST=0" == calc.displayRegisters()
