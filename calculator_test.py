# тестируем калькулятор здесь

from calculator import Calc

calc = Calc()

calc.add("123.456", "789.01")

calc.add("333.0")

print()

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
