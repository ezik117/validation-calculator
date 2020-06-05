# *****************************************************************************
# ПРОЕКТ:    GMP-CALCULATOR
# ФАЙЛ:      appregistry.py
# ЗАГОЛОВОК: КЛАСС РЕЕСТРА КАЛЬКУЛЯТОРА
# ОПИСАНИЕ:  Хранятся общие для разных модулей настройки
# *****************************************************************************

# --------------------- Константы названий флагов -------------------- #

# Константы модуля, используемые также вне модуля (поэтому размещены в реестре).
# Предпочтительно импортировать from flags import <список атрибутов модуля>
# и только необходимые для импортирующего модуля атрибуты
# PI - Procedure Identifier (идентификатор операции - +,-,/,*)
# TODO теоретически надо сделать распаковку констант при импортировании
CD, CONST, EQ, PI = ('CD', 'CONST', 'EQ', 'PI')

# -------------------------- Входные данные -------------------------- #

# WARNING размещение данного списка приводится временно, т.к. он должен
# располагаться за пределами реестра (или создаваться в нем из другого источника)
# Создаем имитацию списка флагов, получаемых из класса, файла, БД и т.п.
# CONFIG Описание конфигурации списка флагов:
# 1) Ключами словаря являются названия базовых флагов калькулятора
# 2) Исключение - запись "combs", которая содержит комбинированные флаги
# 3) Внутри каждого флага есть его описание:
# 		а) запись 'init' - состояние флага при инициализации экземпляра флага
# 		б) запись 'get' - названия getters свойств флага. Причем первое значение
# 		   в списке [0] выводит обратное значение NOT <флаг>, а второе [1] -
# 		   прямое значение <флаг>. Значение None определяет, что свойство
# 		   отсутствует и не имплементируется в класс
# 		в) запись 'set' - список названий setters методов изменения значений флага. Первое значение
# 		   в списке [0] сбрасывает флаг в False, а второе [1] поднимает флаг
# 		   в True. None значения не используются (теоретически они малопригодны).
# 4) Внутри записи 'combs' содержаться названия комбинированных флагов (как ключи словаря)
# 	 и список названий стандартных флагов (значения словаря), из которых состоит комбинированный.
# 	 Комбинированные флаги создаются как <значение [0]> AND <значение [1]>
flagsList = {
	'CD': {
		'init': True,
		'get': ['IS_REG_FILLING', 'IS_NEW_INPUT'],
		'set': ['enable_reg_filling', 'new_reg_filling']
	},
	'CONST': {
		'init': False,
		'get': [None, 'IS_OPS_CONTINUES'],
		'set': ['disable_ops_continues', 'enable_ops_continues']
	},
	'EQ': {
		'init': False,
		'get': [None, 'IS_EQUAL_PRESSED'],
		'set': ['equal_not_pressed', 'equal_pressed']
	},
	'combs': {
		'IS_OPERATION_POSSIBLE': ['IS_REG_FILLING', 'IS_OPS_CONTINUES']
	}
}

# Для сложных флагов, отличных от значений True, False применяем другое описание.
# Фактически здесь только название флага как ключ словаря и значение словаря
# как начальное значение при инициализации экземпляра класса.
eflagsList = {'PI': None}
