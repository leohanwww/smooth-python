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