第十章

from array import array
import reprlib
import math

class Vector:
	typecode = 'd'
	
	def __init__(self, components):
		self._components = array(self.typecode, components)
		
	def __iter__(self):
		return iter(self._components)
		
	def __repr__(self):
		components = reprlib.repr(self._components)
		components = components[components.find('['):-1] # 转换成了str的表示方式
		return 'Vector({})'.format(components)
		# 使用 reprlib.repr() 函数获取 self._components 的有限长度表示形式（如 array('d', [0.0, 1.0, 2.0, 3.0, 4.0, ...])）。
	def __str__(self):
		return str(tuple(self))
		
	def __bytes__(self):
		return bytes([ord(self.typecode)]) + bytes(self._components)
		
	def __eq__(self, other):
		return tuple(self) == tuple(other)
		
	def __abs__(self):
		return math.sqrt(sum(x * x for x in self))
		
	def __bool__(self):
		return bool(abs(self))
		
	@classmethod
	def frombytes(cls, octers):
		typecode = chr(octets[0])
		memv = memoryview(octets[1:]).cast(typecode)
		return cls(memv)
	
协议和鸭子类型
在面向对象编程中，协议是非正式的接口，只在文档中定义，在代码中
不定义。例如，Python 的序列协议只需要 __len__ 和 __getitem__ 两
个方法
我们说它是序列，因为它的行为像序列，这才是重点。称之为鸭子类型

可切片序列
>>> class MySeq:
... def __getitem__(self, index):
...     return index # ➊
...
>>> s = MySeq()
>>> s[1] # ➋
1 
>>> s[1:4] #➌
slice(1, 4, None)
>>> s[1:4:2] # ➍
slice(1, 4, 2)
>>> s[1:4:2, 9] # ➎ 如果有逗号，得到的是元组
(slice(1, 4, 2), 9)
>>> s[1:4:2, 7:9] # ➏ 得到两个切片
(slice(1, 4, 2), slice(7, 9, None))

S.indices(len) -> (start, stop, stride)
indices方法整顿元组，处理缺失索引和负数索引，以及长度超过目标序列的切片，把 start、stop 和 stride 都变成非负数，而且都落在
指定长度序列的边界内。
>>> slice(None, 10, 2).indices(5) # ➊
(0, 5, 2)
>>> slice(-3, None, None).indices(5) # ➋
(2, 5, 1)
❶ 'ABCDE'[:10:2] 等同于 'ABCDE'[0:5:2]
❷ 'ABCDE'[-3:] 等同于 'ABCDE'[2:5:1]

正确处理切片的__getitem__方法

	def __len__(self):
		return len(self._components)
		
	def __getitem__(self, index):
		cls = type(self)
		if instance(index, slice): #判断是不是切片类型
			return cls(self._components[index]) #返回的是vector类型
		elif instance(index, numbers,Intergral): #如果是int类型
			retuen self._components[index] #返回单个值
		else:
			msg = '{cls.__name__} indices must be integers'
			raise TypeError(msg.format(cls=cls)) ➏
			
>>> v7 = Vector(range(7))
>>> v7[-1] ➊
6.0
>>> v7[1:4] ➋
Vector([1.0, 2.0, 3.0])
>>> v7[-1:] ➌
Vector([6.0])
>>> v7[1,2] ➍
Traceback (most recent call last):
...
TypeError: Vector indices must be integers
❶ 单个整数索引只获取一个分量，值为浮点数。
❷ 切片索引创建一个新 Vector 实例。
❸ 长度为 1 的切片也创建一个 Vector 实例。
❹ Vector 不支持多维索引，因此索引元组或多个切片会抛出错误。

动态存储属性
__getattr__方法 
简单来说，对my_obj.x 表达式，Python 会检查 my_obj 实例有没有名为 x 的属性；
如果没有，到类（my_obj.__class__）中查找；如果还没有，顺着继
承树继续查找。
如果依旧找不到，调用 my_obj 所属类中定义的
__getattr__ 方法，传入 self 和属性名称的字符串形式（如 'x'）。
shortcut_names = 'xyzt'
def __getattr__(self, name):
	cls = type(self)
	if len(name) == 1
	pos = cls.shortcut_names.find(name)
	if 0 <= pos < len(self._components)
		return self._components[pos]
	msg = '{.__name__!r} object has no attribute {!r}' ➎
	raise AttributeError(msg.format(cls, name))
	
__getattr__的实现可以支持v.x这样的直接读取属性的方法
__setattr__的实现可以支持v.x = 10 这样的直接赋值方法
如果想允许修改分量，可以使用 __setitem__ 方法，支持 v[0] =
1.1 这样的赋值

散列和快速等值测试
__hash__方法和__eq__方法把实例变成可散列的
import functools
import operator
def __eq__(self, other):
	return tuple(self) == tuple(other)
def __hash__(self):
	hashes = map(hash, self._components)
	return functools.reduce(operator.xor, hashes, 0)

改写的__eq__
def __eq__(self, other):
	if len(self) != len(other)
		return False
	for a, b in zip(self, other):
		if a != b
			return False
	return True
	
def __eq__(self, other):
	return len(self) == len(other) and all(a == b for a, b in zip(self, other))
	

格式化
浮点数的格式代码 'eEfFgGn%'，整数使用的格式代码有 'bcdoxXn'，字符串使用的是
's'。
def __format__(self, fmt_spec=''):
	if fmt_spec.endwith('h') #超球面坐标，超过三个的坐标
		cords = itertools.chain([abs(self)], self.angles()) # 使用 itertools.chain 函数生成生成器表达式，无缝迭代向量的模和各个角坐标。
		outer_fmt='<{}>' #用尖括号表示极坐标
	else:
		cords = self
		outer_fmt = '({})' #用圆括号表示坐标
	components = format((c, fmt_spec) for c in cords) # 创建生成器表达式，按需格式化各个坐标元素。
	return outer_fmt.format(', '.join(components)) # 把以逗号分隔的格式化分量插入尖括号或圆括号。

