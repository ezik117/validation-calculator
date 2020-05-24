# *****************************************************************************
# МОДУЛЬ:    test_flags
# ФАЙЛ:      test_flags.py
# ЗАГОЛОВОК: КЛАСС тестов для класса Flags
# ОПИСАНИЕ:  Класс служит для тестирования через pytest флагов класса Flags
# *****************************************************************************

import pytest
import sys

sys.path.append('..')
from .. import flags as fc

class TestFlags():

# ------------------------- Тестовые функции ------------------------- #

	def test_init(self):
		flag = fc.Flags()
		# Начальная установка флагов
		# assert '0b1' == str(flag)
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == False
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False
	
	# последовательный ввод цифр
	def test_pressed_digital_key(self):
		flag = fc.Flags()
		# Нажата цифра или BS
		flag.equal_not_pressed()
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполняем регистр числа
		flag.enable_reg_filling()
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == False
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == True
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False
		# --- Добавляем к старому ---
		flag.equal_not_pressed()
		# Заполняем регистр числа
		flag.enable_reg_filling()
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == False
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == True
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False
		# --- Нажата BS ---
		flag.equal_not_pressed()
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == False
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == True
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False

	# ввод цифр, затем сброс
	def test_reset_key(self):
		flag = fc.Flags()
		flag.enable_reg_filling()
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == False
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == True
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False
		flag.clear()
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == False
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False

	
	def test_pressed_opcode(self):
		flag = fc.Flags()
		# ввод цифр, затем нажатие какой-либо операции
		flag.equal_not_pressed()
		flag.enable_reg_filling()
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == False
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == True
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажата ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False
		# Можно ли провести операцию ?
		assert flag.IS_OPERATON_POSSIBLE == False
		# введена операция, разрешаем ввод нового числа (или операции)
		flag.new_reg_filling()
		# и отмечаем, что операция не завершена (действует)
		flag.enable_ops_continues()
		# Проверка
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == False
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == True
		assert flag.IS_OPS_STOPPED == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False

		# набираем число
		flag.equal_not_pressed()
		flag.enable_reg_filling()
		# нажимаем операцию
		flag.equal_not_pressed()
		# Можно провести операцию ?
		assert flag.IS_OPERATON_POSSIBLE == True
		# Проверяем вид операции в АЛУ
		assert flag.IS_A_op_B == False
		assert flag.IS_B_op_A == False
		assert flag.IS_NEXT_OPERATION == True
		# После совершения операции в АЛУ ("равно" не нажато)
		flag.new_reg_filling()
		flag.enable_ops_continues()
		# assert str(flag) == '0b11'
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == False
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == True
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False

		return flag

	# нажата "равно" после операции
	def test_equal_after_ops(self):
		flag = self.test_pressed_opcode()
		flag.equal_pressed()
		# assert str(flag) == '0b111'
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == False
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == True
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == True

		assert flag.IS_OPS_CONTINUES == True
		# Проверяем вид операции в АЛУ
		assert flag.IS_B_op_A == True
		assert flag.IS_A_op_B == False
		assert flag.IS_NEXT_OPERATION == False
		flag.new_reg_filling()
		flag.disable_ops_continues()
		# assert str(flag) == '0b101'
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == False
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == True
		return flag
	
	# нажата "равно" после "равно" и последующего набор цифр
	def test_equal_after_eq(self):
		flag = self.test_equal_after_ops()
		# набираем число
		flag.equal_not_pressed()
		flag.enable_reg_filling()
		# assert str(flag) == '0b0'
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == False
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == True
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False
		# нажимаем "равно"
		flag.equal_pressed()
		assert flag.IS_OPS_CONTINUES == False
		# Проверяем вид операции в АЛУ
		assert flag.IS_B_op_A == False
		assert flag.IS_A_op_B == True
		assert flag.IS_NEXT_OPERATION == False
