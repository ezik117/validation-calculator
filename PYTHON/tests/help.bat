﻿
chcp 65001
@echo off
echo ----------------------------------------------------
echo Параметры вызова "test.bat" для выполнения "pytest":
echo      1. help   - описание параметров вызова.
echo      2. add    - запуск "test_calc_alu_add.py". Тестирование в калькуляторе только сложения.
echo      3. flags  - запуск "test_flags.py". Тестирование класса флагов Flags.
echo      4. int    - запуск "test_calculator.py". Тестирование разных операций калькулятора с целыми числами.
echo      5. float  - запуск "test_calc_float.py". Тестирование разных операций калькулятора с дробными числами.
echo      6. num    - запуск "test_bigfloat.py". Тестирование класса больших чисел BigFloat.
echo      7. reg    - запуск "test_registers.py". Тестирование класса регистров Registry.
echo      8. cmp    - запуск "test_compare_bigfloat.py". Тестирование сравнения больших чисел BigFloat, в т.ч. с int и float.
echo      9. sub    - запуск "test_calc_alu_sub.py". Тестирование в калькуляторе только вычитания.
echo     10. abs    - запуск "test_abs_bigfloat.py". Тестирование функции abs в классе BigFloat.
