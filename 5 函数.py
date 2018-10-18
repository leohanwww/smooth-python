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

函数对象内置方法
>>> dir(factorial)
['__annotations__', '__call__', '__class__', '__closure__', '__code__',
'__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
'__format__', '__ge__', '__get__', '__getattribute__', '__globals__',
'__gt__', '__hash__', '__init__', '__kwdefaults__', '__le__', '__lt__',
'__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__',
'__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
'__subclasshook__'] 
函数使用 __dict__ 属性存储赋予它的用户
属性。这相当于一种基本形式的注解。
def factorial(n):
	'''return n!'''
	return 1 if n < 2 else n * factorial(n - 1)

print(factorial.__doc__)
f = factorial
print(f(10), f.__dict__, f.__str__)

>>> return n!
>>> 3628800 {} <method-wrapper '__str__' of function object at 0x00000206DEA219D8>

位置参数、关键字参数、自定义参数
def tag(name, *content, cls=None, **attrs):
"""生成一个或多个HTML标签"""
	if cls is not None:
		attrs['class'] = cls
	if attrs:
		attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
	else:
		attr_str = ''
	if content:
		return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
	else:
		return '<%s%s />' % (name, attr_str)

>>> tag('br') ➊ #传入第一个参数由name获得
'<br />'
>>> tag('p', 'hello') ➋ #第二个传入的参数由*content获得，存入一个元组
'<p>hello</p>'
'<p>world</p>'
>>> tag('p', 'hello', id=33) ➌ #第三个参数id没有定义，存入**attrs，是一个字典
'<p id="33">hello</p>'
>>> print(tag('p', 'hello', 'world', cls='sidebar')) ➍ #cls作为关键字传入
<p class="sidebar">hello</p>
<p class="sidebar">world</p>
>>> tag(content='testing', name="img") ➎ #即便是放在第一个的参数不指定参数名也会被关键字参数*content获得
'<img content="testing" />'
>>> my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 
... 		  'src': 'sunset.jpg', 'cls': 'framed'}
#在 my_tag 前面加上 **，字典中的所有元素作为单个参数传入，同名键会绑定到对应的具名参数上，余下的则被 **attrs 捕获。
>>> tag(**my_tag) ➏
'<img class="framed" src="sunset.jpg" title="Sunset Boulevard" />'

获取关于参数的信息
函数对象有个 __defaults__ 属性，它的值是一个元组，里面保存着定
位参数和关键字参数的默认值。仅限关键字参数的默认值在
__kwdefaults__ 属性中。然而，参数的名称在 __code__ 属性中，它
的值是一个 code 对象引用，自身也有很多属性。

def clip(text, max_len=80):
"""在max_len前面或后面的第一个空格处截断文本
"""
end = None
if len(text) > max_len:
space_before = text.rfind(' ', 0, max_len)
if space_before >= 0:
end = space_before
else:
space_after = text.rfind(' ', max_len)
if space_after >= 0:
end = space_after
if end is None: # 没找到空格
end = len(text)
return text[:end].rstrip()

>>> from clip import clip
>>> clip.__defaults__
(80,)
>>> clip.__code__ 
<code object clip at 0x...>
>>> clip.__code__.co_varnames #参数名称在__code__.co_varnames中
('text', 'max_len', 'end', 'space_before', 'space_after')
>>> clip.__code__.co_argcount #函数参数取前两个
2

使用inspect模块获取函数参数
>>> from clip import clip
>>> from inspect import signature
>>> sig = signature(clip)
>>> sig # doctest: +ELLIPSIS
<inspect.Signature object at 0x...>
>>> str(sig) #
'(text, max_len=80)'
>>> for name, param in sig.parameters.items(): #sig.parameters.items映射了被签名函数的参数
... print(param.kind, ':', name, '=', param.default)
...
POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'>
POSITIONAL_OR_KEYWORD : max_len = 80


>>> import inspect
>>> sig = inspect.signature(tag) ➊
>>> my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
... 'src': 'sunset.jpg', 'cls': 'framed'}
>>> bound_args = sig.bind(**my_tag) ➋ #sig有个bind方法把任意参数绑定到签名中的形参上
>>> bound_args
<inspect.BoundArguments object at 0x...> ➌
>>> for name, value in bound_args.arguments.items(): ➍
... print(name, '=', value)
...
name = img
cls = framed
attrs = {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'}
>>> del my_tag['name'] ➎
>>> bound_args = sig.bind(**my_tag) ➏
Traceback (most recent call last):
...
TypeError: 'name' parameter lacking default value

函数注解
def clip(text:str, max_len:'int > 0'=80) -> str: ➊ #参数注解，后面的是返回值注解
"""在max_len前面或后面的第一个空格处截断文本
"""
end = None
if len(text) > max_len:
space_before = text.rfind(' ', 0, max_len)
if space_before >= 0:
end = space_before
else:
space_after = text.rfind(' ', max_len)
if space_after >= 0:
end = space_after
if end is None: # 没找到空格
end = len(text)
return text[:end].rstrip()
函数声明中的各个参数可以在 : 之后增加注解表达式。如果参数有默认
值，注解放在参数名和 = 号之间。如果想注解返回值，在 ) 和函数声明
末尾的 : 之间添加 -> 和一个表达式。那个表达式可以是任何类型。注
解中最常用的类型是类（如 str 或 int）和字符串（如 'int >
0'）。在示例 5-19 中，max_len 参数的注解用的是字符串。
注解不会做任何处理，只是存储在函数的 __annotations__ 属性（一
个字典）中：
>>> from clip_annot import clip
>>> clip.__annotations__
{'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}

operator模块
可以把算术运算符当作函数使用
使用 reduce 和 operator.mul 函数计算阶乘
from functools import reduce
from operator import mul
def fact(n):
    return reduce(mul, range(1, n+1))

#使用operator里的itemgetter获取参数
>>> metro_data = [
... ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
... ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
... ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
... ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
... ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
... ]
>>>
>>> from operator import itemgetter
>>> for city in sorted(metro_data, key=itemgetter(1)):
... print(city)
...
('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889))
('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
('New York-Newark', 'US', 20.104, (40.808611, -74.020386))

>>> cc_name = itemgetter(1, 0)
>>> for city in metro_data:
... print(cc_name(city))
itemgetter 使用 [] 运算符，因此它不仅支持序列，还支持映射和任
何实现 __getitem__ 方法的类。

使用functools.partial冻结参数
functools.partial 这个高阶函数用于部分应用一个函数。部分应用
是指，基于一个函数创建一个新的可调用对象，把原函数的某些参数固
定。使用这个函数可以把接受一个或多个参数的函数改编成需要回调的
API，这样参数更少
>>> from operator import mul
>>> from functools import partial
>>> triple = partial(mul, 3) ➊ #其实就是指定一个参数的默认值
>>> triple(7) ➋
21