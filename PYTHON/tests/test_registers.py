# *****************************************************************************
# МОДУЛЬ:    test_registers
# ФАЙЛ:      test_registers.py
# ЗАГОЛОВОК: КЛАСС тестов для регистров
# ОПИСАНИЕ:  Класс служит для тестирования через pytest класса Registry
# *****************************************************************************

import pytest
import sys

sys.path.append('..')
from .. import flags
from .. import registers

class TestRegisters():

	# ------------------------- Тестовые функции ------------------------- #

	# инициализация числа
	def test_initial(self):
		reg = registers.Registry('A')
		assert 'A' == reg.name
		assert '0' == reg.value
		return reg

	# добавление цифр, точки
	# @pytest.mark.skip()
	def test_input(self):
		reg = self.test_initial()
		flag = flags.Flags()
		reg.input('5', flag)
		assert '5' == str(reg.value)
		flag.ENABLE_REG_FILLING
		reg.input('4', flag)
		assert '54' == str(reg.value)
		reg.input('.', flag)
		assert '54.0' == str(reg.value)
		reg.input('2', flag)
		assert '54.2' == str(reg.value)
		reg.input('7', flag)
		assert '54.27' == str(reg.value)
		return reg

	# затереть последние смиволы
	# @pytest.mark.skip()
	def test_backspace(self):
		reg = self.test_input()
		reg.BS()
		assert '54.2' == str(reg.value)
		reg.BS()
		assert '54.0' == str(reg.value)
		reg.BS()
		assert '54' == str(reg.value)
		reg.BS()
		assert '5' == str(reg.value)
		reg.BS()
		assert '0' == str(reg.value)
		reg.BS()
		assert '0' == str(reg.value)
		return reg

	# проверить на первую точку
	# @pytest.mark.skip()
	def test_first_point(self):
		reg = self.test_initial()
		flag = flags.Flags()
		reg.input('.', flag)
		assert '0.0' == str(reg.value)
		flag.ENABLE_REG_FILLING
		reg.input('2', flag)
		assert '0.2' == str(reg.value)
		reg.input('7', flag)
		assert '0.27' == str(reg.value)

	# проверка ввода первых нулей
	# @pytest.mark.skip()
	def test_first_zero(self):
		reg = self.test_initial()
		flag = flags.Flags()
		# сейчас CD=1 (новый ввод)
		reg.input('0', flag)
		assert '0' == str(reg.value)
		# CD опять не меняется (из-за проверки 0 в pressedDigitalKey)
		reg.input('0', flag)
		assert '0' == str(reg.value)
		# CD опять не меняется (из-за проверки 0 в pressedDigitalKey)
		reg.input('.', flag)
		assert '0.0' == str(reg.value)
		# теперь CD=0
		flag.ENABLE_REG_FILLING
		reg.BS()
		assert '0' == str(reg.value)
		# TODO что с CD ? (должен регулироваться калькулятором)
