第二章 序列构成的数组

python序列的风格 迭代 切片 排序 拼接

容器序列
　　list、tuple 和 collections.deque 这些序列能存放不同类型的数据。

扁平序列
　　str、bytes、bytearray、memoryview 和 array.array，这类序列只能容纳一种类型。

容器序列存放的是它们所包含的任意类型的对象的引用，而扁平序列
里存放的是值而不是引用。换句话说，扁平序列其实是一段连续的内存
空间。

可变序列
　　list、bytearray、array.array、collections.deque 和
memoryview。
不可变序列
　　tuple、str 和 bytes。


列表推导式
>>> symbols = '$¢£¥€¤'
>>> codes = [ord(symbol) for symbol in symbols]
>>> codes
[36, 162, 163, 165, 8364, 164]
列表推导式不宜过长，可以用for改写，倒是没有什么硬性规定，依靠习惯
列表推导式创建新的列表

使用列表推导计算笛卡儿积
>>> colors = ['black', 'white']
>>> sizes = ['S', 'M', 'L']
>>> tshirts = [(color, size) for color in colors for size in sizes] 
#从出来的结果看，是以for color in colors来排列的
>>> tshirts
[('black', 'S'), ('black', 'M'), ('black', 'L'), ('white', 'S'),
('white', 'M'), ('white', 'L')]

生成器表达式，列表推导式只能生成列表，而生成器可以生成其他类型的序列
>>> symbols = '$¢£¥€¤'
>>> tuple(ord(symbol) for symbol in symbols) ➊
(36, 162, 163, 165, 8364, 164)
>>> import array
>>> array.array('I', (ord(symbol) for symbol in symbols)) ➋
array('I', [36, 162, 163, 165, 8364, 164])
生成笛卡儿积
>>> colors = ['black', 'white']
>>> sizes = ['S', 'M', 'L']
>>> for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes): ➊
... print(tshirt)
...
black S
black M
black L
white S
white M
white L

元组
把元组用作记录
>>> lax_coordinates = (33.9425, -118.408056) ➊
>>> city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014) ➋ #典型元组拆包
>>> traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ➌
... ('ESP', 'XDA205856')]
>>> for passport in sorted(traveler_ids): ➍
... print('%s/%s' % passport) ➎
...
BRA/CE342567
ESP/XDA205856
USA/31195855
>>> for country, _ in traveler_ids: ➏ #_占位符，也叫元组拆包
... print(country)
...
USA
BRA
ESP

还可以用 * 运算符把一个可迭代对象拆开作为函数的参数：
>>> divmod(20, 8)
(2, 4)
>>> t = (20, 8)
>>> divmod(*t)
(2, 4)
>>> quotient, remainder = divmod(*t)
>>> quotient, remainder
(2, 4)

>>> import os
>>> _, filename = os.path.split('/home/luciano/.ssh/idrsa.pub')
>>> filename
'idrsa.pub'

用*来处理剩下的元素
>>> a, b, *rest = range(5)
>>> a, b, rest
(0, 1, [2, 3, 4])
>>> a, b, *rest = range(3)
>>> a, b, rest
(0, 1, [2])
>>> a, b, *rest = range(2)
>>> a, b, rest
(0, 1, [])
在平行赋值中，* 前缀只能用在一个变量名前面，但是这个变量可以出
现在赋值表达式的任意位置：
>>> a, *body, c, d = range(5)
>>> a, body, c, d
(0, [1, 2], 3, 4)
>>> *head, b, c, d = range(5)
>>> head, b, c, d
([0, 1], 2, 3, 4)

具名元组
它可以用来构建一个带字段名的元组和一个有名字的类——这个带名字的类对调试程序有很大帮助。
from collections import namedtuple
>>> City = namedtuple('City', 'name country population coordinates')
>>> beijing = City('Beijing', 'china', 36.933, (35.689722, 139.691667))
>>> beijing.population
>>> 36.933
创建具名元组和创建一个类一样，要有类名和参数
具名元组的方法
>>> City._fields ➊
('name', 'country', 'population', 'coordinates')
>>> LatLong = namedtuple('LatLong', 'lat long')
>>> delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
>>> delhi = City._make(delhi_data) ➋ 或 delhi = City(*delhi_data)
>>> delhi._asdict() ➌
OrderedDict([('name', 'Delhi NCR'), ('country', 'IN'), ('population',
21.935), ('coordinates', LatLong(lat=28.613889, long=77.208889))])
>>> for key, value in delhi._asdict().items():
print(key + ':', value)
name: Delhi NCR
country: IN
population: 21.935
coordinates: LatLong(lat=28.613889, long=77.208889)
>>>
❶ _fields 属性是一个包含这个类所有字段名称的元组。
❷ 用 _make() 通过接受一个可迭代对象来生成这个类的一个实例，它
的作用跟 City(*delhi_data) 是一样的。
❸ _asdict() 把具名元组以 collections.OrderedDict 的形式返
回，我们可以利用它来把元组里的信息友好地呈现出来。

切片

对对象进行切片
s[start:stop:step]
python对序列求值的时候，调用的是seq.__getitem__(slice(start:stop:step))
切片时这么使用item[slice(start:stop:step)]

给切片赋值
>>> l = list(range(10))
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> l[2:5] = [20, 30]
>>> l
[0, 1, 20, 30, 5, 6, 7, 8, 9]
>>> del l[5:7]
>>> l
[0, 1, 20, 30, 5, 8, 9]
>>> l[3::2] = [11, 22]
>>> l
[0, 1, 20, 11, 5, 22, 9]
>>> l[2:5] = 100 ➊
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: can only assign an iterable
2
2
>>> l[2:5] = [100]
>>> l
[0, 1, 100, 22, 9]
➊ 如果赋值的对象是一个切片，那么赋值语句的右侧必须是个可迭代
对象。即便只有单独一个值，也要把它转换成可迭代的序列。

序列的拼接 + *
用 * 来初始化由列表组成的列表
>>> board = [['_'] * 3 for i in range(3)]
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> board[1][2] = 'x'
>>> board
[['_', '_', '_'], ['_', '_', 'x'], ['_', '_', '_']]

序列的增量赋值 += *=
+= 背后的特殊方法是 __iadd__ （用于“就地加法”）。但是如果一个类
没有实现这个方法的话，Python 会退一步调用 __add__
>>> a += b
如果 a 实现了 __iadd__ 方法，就会调用这个方法。。同时对可变序列
（例如 list、bytearray 和 array.array）来说，a 会就地改动,就
像调用了 a.extend(b) 一样。但是如果 a 没有实现 __iadd__ 的话，a
+= b 这个表达式的效果就变得跟 a = a + b 一样了：首先计算 a +
b，得到一个新的对象，然后赋值给 a。也就是说，在这个表达式中，
变量名会不会被关联到新的对象，完全取决于这个类型有没有实现
__iadd__ 这个方法。

list.sort方法和内置函数sorted
list.sort方法就地排序，并返回None
内置函数sorted创建一个新列表作为返回值，这个方法可以接受任何形式的可迭代对象作为参数，
甚至包括不可变序列或生成器。而不管 sorted 接受的是怎样的参
数，它最后都会返回一个列表。
参数 reverse 
     key  一个只有一个参数的函数 可以是key = str.lower() key = len

bisect模块

bisect.bisect_left(a, x, lo=0, hi=len(a))
Locate the insertion point for x in a to maintain sorted order. 定位插入数字x位于a的哪个位置，返回定位到的位置的值
>>> b = [2, 4, 6, 8, 10]
>>> bisect.bisect(b, 5)
2 #在第二个数字的left位
>>> b
[2, 4, 6, 8, 10]

根据一个分数，找到它所对应的成绩
>>> def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
... i = bisect.bisect(breakpoints, score)
... return grades[i]
...
>>> [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
['F', 'A', 'C', 'C', 'B', 'A', 'A']

bisect.insort(a, x, lo=0, hi=len(a))
Insert x in a in sorted order. 把x插入到有序序列a中，原地插入，改变原来的序列

>>> x = 7
>>> bisect.insort(b, x)
>>> b
[2, 4, 6, 7, 8, 10]

数组
数组有类似列表的方法，还有自有方法.frombytes .tofile
from array import array
f = array('d', (random() for i in range(10**5)))
with open('floats.bin', 'wb') as fp
f.tofile(fp) 写到文件
f2 = array('d') 空数组
f2.fromfile(fp, 10**5) 从文件读取

b = array.array(a.typecode, sorted(a))

Type code	C Type	Python Type	Minimum size in bytes	Notes
'b'	signed char	int	1	 
'B'	unsigned char	int	1	 
'u'	Py_UNICODE	Unicode character	2	(1)
'h'	signed short	int	2	 
'H'	unsigned short	int	2	 
'i'	signed int	int	2	 
'I'	unsigned int	int	2	 
'l'	signed long	int	4	 
'L'	unsigned long	int	4	 
'q'	signed long long	int	8	(2)
'Q'	unsigned long long	int	8	(2)
'f'	float	float	4	 
'd'	double	float	8	 

memoryview
memoryview 是一个内置类，它能让用户在不复制内容的情况下操作同
一个数组的不同切片

>>> data = bytearray(b'abcefg')
>>> v = memoryview(data)
>>> v[0] = ord(b'z') 改变memoryview
>>> data
bytearray(b'zbcefg') 原来的data也随之改变了

