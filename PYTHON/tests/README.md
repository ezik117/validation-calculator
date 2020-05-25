# Описание тестовых файлов и команд тестов для калькулятора
Для тестирования калькулятора применяются модули с классами тестов, написанные для **pytest** и используемые для тестирования каждой функции или класса калькулятора отдельно.
____
## Оглавление
1. [Файл помощи _help.bat_](#help)
2. [Файл запускаемых тестов _test.bat_](#test)
3. [Тестирование составных частей калькулятора (классов)](#classes):
    - [Тест класса флагов _Flags_](#flags)
    - [Тест класса регистров _Registry_](#registry)
    - [Тест класса чисел _BigFloat_](#bigfloat)
4. [Тестирование отдельных методов класса _BigFloat_](#methods):
    - [Тест методов сравнения чисел](#compare)
    - [Тест метода вычисления модуля числа _abs( )_](#abs)
5. [Первичное тестирование действий класса _Calculator_](#first):
    - [Тест работоспособности калькулятора с целыми числами](#int)
    - [Тест работоспособности калькулятора с дробными числами](#float)
    - [Тест сложения положительных чисел](#add)
    - [Тест сложения отрицательных чисел](#_add)
    - [Тест вычитания положительных чисел](#sub)
5. [Базовое тестирование действий класса _Calculator_](#base):
    - [Тест всех вариантов операции сложения](#all_add)
    - [Тест всех вариантов операции вычитания](#all_sub)
    - [Совместный тест всех вариантов операции сложения и вычитания](#all)
___
## <a id="help"></a> Файл помощи `help.bat`
Файл содержит описание команд файла `test.bat`, запускаемых командой вида `test cmd`.
Сам файл помощи запускается командами `test --help`, `test help` или `test -h`.
___
## <a id="test"></a> Файл запускаемых тестов `test.bat`
Файл содержит команды вида `test cmd` для запуска тестов **pytest**.
___
## <a id="classes"></a> Тестирование составных частей калькулятора
В этих тестах тестируются отдельные классы калькулятора, которые используются для построения программы.
___
#### <a id="flags"></a> _flags_ - тест класса флагов `Flags`
Тестируется инициализация, различные комбинации флагов для работы калькулятора.
#### <a id="registry"></a> _reg_ - тест класса регистров `Registry`
Тестируется инициализация, ввода чисел в регистр, затирание символа Backspace, ввод точки, ввод нуля.
#### <a id="bigfloat"></a> _num_ - тест класса чисел `BigFloat`
Тестируется создание экземпляра класса большого числа _BigFloat_, ввод числа (в т.ч. дробного), затирание последнего символа Backspace, ввод нуля, запятой дробного числа, некоторые методы сравнения чисел.
___
## <a id="methods"></a> Тестирование отдельных методов класса BigFloat
Тестируются отдельные методы класса больших чисел BigFloat (в основном специальные).
___
#### <a id="compare"></a> _cmp_ - тест класса флагов `Flags`
Тестируется равенство, неравенство, различные варианты сравнения чисел BigFloat друг с другом и числами классов _int_ и _float_, в том числе с отрицательными.
#### <a id="abs"></a> _abs_ - тест класса регистров `Registry`
Тестируется метод получения модуля числа (положительного, отрицательного и нуля).
___
## <a id="first"></a> Первичное тестирование действий класса `Calculator`
Тестируется работа калькулятора с целыми и дробными числами, некоторые варианты сложения и вычитания. Использовались для первоначального тестирования калькулятора. Могут быть удалены в будущем или преобразованы.
___
#### <a id="int"></a> _int_ - тест работы калькулятора с целыми числами
Тестируются ввод целых чисел, очистка калькулятора, стирание символа Backspace, различные действия с числами.
#### <a id="float"></a> _float_ - тест работы калькулятора с дробными числами
Тестируются ввод дробных чисел, очистка калькулятора, стирание символа Backspace, различные действия с числами, ошибка ввода второй запятой.
#### <a id="add"></a> _add_ - первичный тест сложения положительных чисел
Тестируются различные режимы внутренней работа калькуляторы при сложении положительных чисел.
#### <a id="_add"></a> _-add_ - первичный тест сложения отрицательных чисел
Тестируются различные режимы внутренней работа калькуляторы при сложении отрицательных чисел.
#### <a id="sub"></a> _sub_ - первичный тест вычитания положительных чисел
Тестируются различные режимы внутренней работа калькуляторы при вычитании положительных чисел.
___
## <a id="base"></a> Базовое тестирование действий класса `Calculator`
___
#### <a id="all_add"></a> _+all_ - тест всех вариантов сложения
Тестируются все возможные комбинации сложения, которые можно набрать в калькуляторе вручную, положительных и отрицательных чисел.
#### <a id="all_sub"></a> _-all_ - тест всех вариантов вычитания
Тестируются все возможные комбинации вычитания, которые можно набрать в калькуляторе вручную, положительных и отрицательных чисел.
#### <a id="all"></a> _all_ - совместный тест всех вариантов сложения и вычитания
Тестируются все возможные комбинации сложения и вычитания, которые можно набрать в калькуляторе вручную, положительных и отрицательных чисел. Это объединение двух предыдущих тестов в одной команде.
___