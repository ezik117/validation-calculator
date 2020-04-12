import pytest
# from . import flags as fc

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
		flag.EQUAL_NOT_PRESSED
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == True
		# Заполняем регистр числа
		flag.ENABLE_REG_FILLING
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == False
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == True
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False
		# --- Добавляем к старому ---
		flag.EQUAL_NOT_PRESSED
		# Заполняем регистр числа
		flag.ENABLE_REG_FILLING
		# Ввод нового числа ?
		assert flag.IS_NEW_INPUT == False
		# Заполнение старого числа ?
		assert flag.IS_REG_FILLING == True
		# Есть ли незавершенная операция операция ?
		assert flag.IS_OPS_CONTINUES == False
		# Нажати ли клавиша "равно" ?
		assert flag.IS_EQUAL_PRESSED == False
		# --- Нажата BS ---
		flag.EQUAL_NOT_PRESSED
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
		flag.ENABLE_REG_FILLING
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
		flag.EQUAL_NOT_PRESSED
		flag.ENABLE_REG_FILLING
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
		flag.NEW_REG_FILLING
		# и отмечаем, что операция не завершена (действует)
		flag.ENABLE_OPS_CONTINUES
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
		flag.EQUAL_NOT_PRESSED
		flag.ENABLE_REG_FILLING
		# нажимаем операцию
		flag.EQUAL_NOT_PRESSED
		# Можно провести операцию ?
		assert flag.IS_OPERATON_POSSIBLE == True
		# Проверяем вид операции в АЛУ
		assert flag.IS_A_op_B == False
		assert flag.IS_B_op_A == False
		assert flag.IS_NEXT_OPERATION == True
		# После совершения операции в АЛУ ("равно" не нажато)
		flag.NEW_REG_FILLING
		flag.ENABLE_OPS_CONTINUES
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
		flag.EQUAL_PRESSED
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
		flag.NEW_REG_FILLING
		flag.DISABLE_OPS_CONTINUES
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
		flag.EQUAL_NOT_PRESSED
		flag.ENABLE_REG_FILLING
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
		flag.EQUAL_PRESSED
		assert flag.IS_OPS_CONTINUES == False
		# Проверяем вид операции в АЛУ
		assert flag.IS_B_op_A == False
		assert flag.IS_A_op_B == True
		assert flag.IS_NEXT_OPERATION == False
