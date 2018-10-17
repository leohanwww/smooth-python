第五章

在 Python 中，函数是一等对象。编程语言理论家把“一等对象”定义为满
足下述条件的程序实体：
在运行时创建
能赋值给变量或数据结构中的元素
能作为参数传给函数
能作为函数的返回结果

创建并测试一个函数，然后读取它的 __doc__ 属性，再
检查它的类型
>>> def factorial(n): ➊
... '''returns n!'''
... return 1 if n < 2 else n * factorial(n-1)
...
>>> factorial(42)
1405006117752879898543142606244511569936384000000000
>>> factorial.__doc__ ➋
'returns n!'
>>> type(factorial) ➌
<class 'function'>

通过别的名称使用函数，再把函数作为参数传递
>>> fact = factorial
>>> fact
<function factorial at 0x...>
>>> fact(5)
120
>>> map(factorial, range(11))
<map object at 0x...>
>>> list(map(fact, range(11)))
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]

高阶函数
接受函数为参数，或者把函数作为结果返回的函数是高阶函数

根据反向拼写给一个单词列表排序
>>> def reverse(word):
... return word[::-1]
>>> reverse('testing')
'gnitset'
>>> sorted(fruits, key=reverse)
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']

计算阶乘列表：map 和 filter 与列表推导比较
>>> list(map(fact, range(6))) ➊
[1, 1, 2, 6, 24, 120]
>>> [fact(n) for n in range(6)] ➋
[1, 1, 2, 6, 24, 120]
>>> list(map(factorial, filter(lambda n: n % 2, range(6)))) ➌
[1, 6, 120]
>>> [factorial(n) for n in range(6) if n % 2] ➍
[1, 6, 120]

使用 reduce 和 sum 计算 0~99 之和
>>> from functools import reduce ➊
>>> from operator import add ➋
>>> reduce(add, range(100)) ➌
4950
>>> sum(range(100)) ➍
4950

匿名函数
lambda 函数的定义体只能使用纯表达
式。换句话说，lambda 函数的定义体中不能赋值，也不能使用 while
和 try 等 Python 语句。在参数列表中最适合使用匿名函数
>>> fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
>>> sorted(fruits, key=lambda word: word[::-1])
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']

可调用对象
如果想判断对象能否调用，可以使用内置的 callable() 函数。
Python 数据模型文档列出了 7 种可调用对象。
用户定义的函数
　　使用 def 语句或 lambda 表达式创建。
内置函数
　　使用 C 语言（CPython）实现的函数，如 len 或 time.strftime。
内置方法
　　使用 C 语言实现的方法，如 dict.get。
方法
　　在类的定义体中定义的函数。
类
　　调用类时会运行类的 __new__ 方法创建一个实例，然后运行
__init__ 方法，初始化实例，最后把实例返回给调用方。因为 Python
没有 new 运算符，所以调用类相当于调用函数。（通常，调用类会创建
那个类的实例，不过覆盖 __new__ 方法的话，也可能出现其他行为。
19.1.3 节会见到一个例子。）
类的实例
　　如果类定义了 __call__ 方法，那么它的实例可以作为函数调用。
生成器函数
   使用 yield 关键字的函数或方法。调用生成器函数返回的是生成
器对象。

只要实现了__call__方法，任何python对象都可以表现得像函数
import random
class BingoCage:

def __init__(self, items):
	self._items = list(items) ➊
	random.shuffle(self._items) ➋ #打乱顺序
	
def pick(self): ➌
	try:
		return self._items.pop()
	except IndexError:
		raise LookupError('pick from empty BingoCage') ➍
		
def __call__(self): ➎
	return self.pick()

>>> bingo = BingoCage(range(3))
>>> bingo.pick()
1 
>>> bingo()
0 
>>> callable(bingo)
True