# тестируем калькулятор здесь

from calculator import Calc

calc = Calc()

print("load registy testing...")
calc.add("123.456", "789.01")
calc.add("333.0")

print("stack testing 1...")
calc._Calc__stackPush(1)
calc._Calc__stackPush(2)
calc._Calc__stackPush(3)

print(calc._Calc__stackPop())
print(calc._Calc__stackPop())
print(calc._Calc__stackPop())

print("stack testing 2...")
calc._Calc__stackPush(1)
calc._Calc__stackPush(2)
calc._Calc__stackPush(3)

calc._Calc__stackClear()
print(calc._Calc__stackPop())

print("stack testing 3...")
calc._Calc__stackPush(1)
calc._Calc__stackPush(2)
calc._Calc__stackPush(3)

calc._Calc__stackClear(2)
print(calc._Calc__stackPop())

print("stack testing 4...")
calc._Calc__stackPush(1)
calc._Calc__stackPush(2)
calc._Calc__stackPush(3)

print(calc._Calc__stackGet(2))
print(calc._Calc__stackGet())

print('--- regisry class ---')

# тестируем регистры здесь

from calculator import Registry

r = Registry()

r.load("-123.45")
print(r.buildString(raw=True))

r.align("_integer", 5)
r.align("_fractional", 5)
print(r.buildString(raw=True))

r.reset()
print(r.buildString(raw=True))

