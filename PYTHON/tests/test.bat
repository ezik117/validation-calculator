@echo off

if "%1" == "" help.bat
if %1 == add pytest -v test_calc_alu_add.py
if %1 == sign pytest -v test_calc_sign_add.py
if %1 == sub pytest -v test_calc_alu_sub.py
if %1 == flags pytest -v test_flags.py
if %1 == int pytest -v test_calculator.py
if %1 == float pytest -v test_calc_float.py
if %1 == num pytest -v test_bigfloat.py
if %1 == reg pytest -v test_registers.py
if %1 == cmp pytest -v test_compare_bigfloat.py
if %1 == abs pytest -v test_abs_bigfloat.py
if %1 == +all pytest -v test_calc_all_add.py
if %1 == -all pytest -v test_calc_all_sub.py
if %1 == help help.bat