import pytest
import sys

sys.path.append('..')
from .. import flags as fc

class TestFlags():

# ------------------------- Тестовые функции ------------------------- #

	def test_init(self):
		flag = fc.Flags()
		# Начальная установка флагов
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == False
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False

		# компактная проверка флагов: CD, CONST, EQ
		assert flag.check() == (True, False, False)
		# компактная проверка флагов в битовом виде (обратный порядок) - EQ, CONST, CD
		assert flag.control() == '001'
