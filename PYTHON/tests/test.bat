@echo off

if "%1" == "" help.bat
if %1 == add pytest -v test_calc_alu_add.py
if %1 == flags pytest -v test_flags.py
if %1 == int pytest -v test_calculator.py
if %1 == float pytest -v test_calc_float.py
if %1 == help help.bat