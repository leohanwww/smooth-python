第九章

对象表现形式
__repr__、__str__ 和 __format__ 都必须返回 Unicode 字
符串（str 类型）。只有 __bytes__ 方法应该返回字节序列
（bytes 类型）。

from array import array
import math

class Vector2d:
	typecode = 'd' #类属性，方法__bytes__转换字节序列时使用
	
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)
		
	def __iter__(self): #把实例变成可迭代对象，可以拆包
		return (i for i in (self.x, self.y))
		
	def __repr__(self):
		class_name = type(self).__name__
		return '{}({!r}, {!r})'.format(class_name, *self)
		# 因为 Vector2d 实例是可迭代的对象，所以 *self 会把x 和 y 分量提供给 format 函数。
	def __str__(self):
		return str(tuple(self))
		# 供print(v1)函数调用
	def __bytes__(self):
		return (bytes([ord(self.typecode)]) + 
		         bytes(array(self.typecode, self)))
		#>>> octets = bytes(v1) 显示成
		#>>> octets
		#b'd\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
	def __eq__(self, other):
		return tuple(self) == tuple(other)
		
	def __abs__(self):
		return math.hypot(self.x, self.y)
		
	def __bool__
		return bool(abs(self))
		
>>> v1 = Vector2d(3, 4)
>>> print(v1.x, v1.y) ➊
3.0 4.0
>>> x, y = v1 ➋
>>> x, y
(3.0, 4.0)
>>> v1 ➌
Vector2d(3.0, 4.0)
>>> v1_clone = eval(repr(v1)) ➍
>>> v1 == v1_clone ➎
True
>>> print(v1) ➏
(3.0, 4.0)
>>> octets = bytes(v1) ➐
>>> octets
b'd\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
>>> abs(v1) ➑
5.0
>>> bool(v1), bool(Vector2d(0, 0)) ➒

备选构造方法
把Vector2d从字节序列转换成为实例
@classmethod # 类方法使用 classmethod 装饰器修饰。
def frombytes(cls, octets): # 不用传入 self 参数；相反，要通过 cls 传入类本身。
	typecode = chr(octets[0]) # 从第一个字节中读取 typecode
	memv = memoryview(octets[1:]).cast(typecode)
	# 使用传入的 octets 字节序列创建一个 memoryview，然后使用typecode转换。
	return cls(*memv) # 拆包转换后的 memoryview，得到构造方法所需的一对参数。构建一个新的实例
	
v2 = Vector2d.frombytes(octets)

classmethod和staticmethod

class Demo:
... @classmethod
... def klassmeth(*args):
... 	return args # ➊ # 返回全部位置参数
... @staticmethod
... def statmeth(*args):
... 	return args # ➋
...
>>> Demo.klassmeth() # ➌ # 第一个参数始终是 Demo 类
(<class '__main__.Demo'>,)
>>> Demo.klassmeth('spam')
(<class '__main__.Demo'>, 'spam')
>>> Demo.statmeth() # ➍ # 静态方法类似普通函数
()
>>> Demo.statmeth('spam')
('spam',)
其实，静态方法就是普通的函数，只是碰巧在类的定义体
中，而不是在模块层定义

格式化显示

>>> brl = 1/2.43 # BRL到USD的货币兑换比价
>>> brl
0.4115226337448559
>>> format(brl, '0.4f') # ➊
'0.4115'
>>> '1 BRL = {rate:0.2f} USD'.format(rate=brl) # ➋
'1 BRL = 0.41 USD'
# str.format()形式


格式微语言
%s    字符串 (采用str()的显示)
%r    字符串 (采用repr()的显示)
%c    单个字符
%b    二进制整数
%d    十进制整数
%i    十进制整数
%o    八进制整数
%x    十六进制整数
%e    指数 (基底写为e)
%E    指数 (基底写为E)
%f    浮点数
%F    浮点数，与上相同%g    指数(e)或浮点数 (根据显示长度)
%G    指数(E)或浮点数 (根据显示长度)
%%    字符"%"

>>> print("%+10x" % 10)
    +a
x 为表示 16 进制，显示宽度为 10，前面有 8 个空格。

>>>print("%-5x" % -10)
-a   
%-5x 负号为左对齐，显示宽度为 5，故 -a 后面有 3 个空格

str.format()

>>> print('This {food} is {adjective}.'.format(
...       food='spam', adjective='absolutely horrible'))
This spam is absolutely horrible.
位置参数{0} {1}
>>> import math
>>> print('The value of PI is approximately {0:.3f}.'.format(math.pi))
The value of PI is approximately 3.142.
# .3 是小数位数

!a (应用 ascii())， !s （应用 str() ）和 !r （应用 repr() ）可以在格式化之前转换值:
>>> import math
>>> print('The value of PI is approximately {}.'.format(math.pi))
The value of PI is approximately 3.14159265359.
>>> print('The value of PI is approximately {!r}.'.format(math.pi))
The value of PI is approximately 3.141592653589793.

>>> table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
>>> for name, phone in table.items():
...     print('{0:10} ==> {1:10d}'.format(name, phone))
...
Jack       ==>       4098
Dcab       ==>       7678
Sjoerd     ==>       4127
#{}中的0和1是位置参数，:10是宽度
终极写法{1:10.3f} 位置参数，宽度参数，小数位数参数,类型

def __format__(self, fmt=''):
	compents = (format(c, fmt) for c in self)
	# 使用内置的 format 函数把 fmt_spec 应用到向量的各个分量上，构建一个可迭代的格式化字符串。
	return '({}, {})'.format(*compents)
	# 把格式化字符串代入公式 '(x, y)' 中。
	
>>> v1 = Vector2d(3, 4)
>>> format(v1)
'(3.0, 4.0)'
>>> format(v1, '.2f')
'(3.00, 4.00)'