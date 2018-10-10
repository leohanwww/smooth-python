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