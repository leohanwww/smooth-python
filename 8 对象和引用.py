第八章

变量是对一段内存的引用

>>> class Gizmo:
... def __init__(self):
... print('Gizmo id: %d' % id(self))
...
>>> x = Gizmo()
Gizmo id: 4301489152 ➊
>>> y = Gizmo() * 10 ➋
Gizmo id: 4301489432 ➌
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for *: 'Gizmo' and 'int'
>>>
>>> dir() ➍
['Gizmo', '__builtins__', '__doc__', '__loader__', '__name__',
'__package__', '__spec__', 'x']
变量y不会创建因为赋值前就抛出了异常，但是右边的类却创建了
为了理解 Python 中的赋值语句，应该始终先读右边。对象在
右边创建或获取，在此之后左边的变量才会绑定到对象上，这就像
为对象贴上标注

== 运算符比较两个对象的值（对象中保存的数据），而 is 比较对象的
标识。
x is None
x is not None
is 运算符比 == 速度快，因为它不能重载，所以 Python 不用寻找并调用
特殊方法，而是直接比较两个整数 ID
a == b 是语法糖，等同于
a.__eq__(b) 继承自 object 的 __eq__ 方法比较两个对象的 ID，结
果与 is 一样。但是多数内置类型使用更有意义的方式覆盖了 __eq__
方法
而 str、bytes 和 array.array 等单一类型序列是扁平的，它们保存的不是引用，而是在连
续的内存中保存数据本身（字符、字节和数字）。
元组的可散列条件是里面的元素都是不可变的，不是所有元组都是可散列的

浅复制是默认的
>>> l1 = [3, [55, 44], (7, 8, 9)]
>>> l2 = list(l1) ➊ #用list其实创建了一个新对象l2，l4 = l1[:]同理
>>> l2
[3, [55, 44], (7, 8, 9)]
>>> l2 == l1 ➋
True
>>> l2 is l1 ➌
False
浅复制（即复制了最外层容器，副本中
的元素是源容器中元素的引用）

为任意对象做深复制和浅复制
class Bus:
def __init__(self, passengers=None):
	if passengers is None:
		self.passengers = []
	else:
		self.passengers = list(passengers)
def pick(self, name):
	self.passengers.append(name)
def drop(self, name):
	self.passengers.remove(name)
	
>>> import copy
>>> bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
>>> bus2 = copy.copy(bus1) #浅复制
>>> bus3 = copy.deepcopy(bus1) #深复制
>>> id(bus1), id(bus2), id(bus3)
(4301498296, 4301499416, 4301499752) ➊
>>> bus1.drop('Bill')
>>> bus2.passengers
['Alice', 'Claire', 'David'] ➋ #bus1下客后，bus2也少了乘客
>>> id(bus1.passengers), id(bus2.passengers), id(bus3.passengers)
(4302658568, 4302658568, 4302657800) ➌
>>> bus3.passengers
['Alice', 'Bill', 'Claire', 'David'] ➍ #深复制用了另外一个列表

函数的参数作为引用
Python 唯一支持的参数传递模式是共享传参（call by sharing）
共享传参指函数的各个形式参数获得实参中各个引用的副本。也就是
说，函数内部的形参是实参的别名。

不要使用可变类型作为参数的默认值
class HauntedBus:
	"""备受幽灵乘客折磨的校车"""
	def __init__(self, passengers=[]): ➊
		self.passengers = passengers ➋
	def pick(self, name):
		self.passengers.append(name) ➌
	def drop(self, name):
		self.passengers.remove(name)
		
❶ 如果没传入 passengers 参数，使用默认绑定的列表对象，一开始
是空列表。
❷ 这个赋值语句把 self.passengers 变成 passengers 的别名，而没
有传入 passengers 参数时，后者又是默认列表的别名。
❸ 在 self.passengers 上调用 .remove() 和 .append() 方法时，修
改的其实是默认列表，它是函数对象的一个属性。
>>> bus1 = HauntedBus(['Alice', 'Bill'])
>>> bus1.passengers
['Alice', 'Bill']
>>> bus1.pick('Charlie')
>>> bus1.drop('Alice')
>>> bus1.passengers ➊
['Bill', 'Charlie']
>>> bus2 = HauntedBus() ➋
>>> bus2.pick('Carrie')
>>> bus2.passengers
['Carrie']
>>> bus3 = HauntedBus() ➌
>>> bus3.passengers ➍
['Carrie']
>>> bus3.pick('Dave')
>>> bus2.passengers ➎
['Carrie', 'Dave']
>>> bus2.passengers is bus3.passengers ➏
True
>>> bus1.passengers ➐
['Bill', 'Charlie']
这些实例共享了类的passengers的参数，发生了错误
问题是，bus2.passengers 和 bus3.passengers 指代同一个列
表。
出现这个问题的根源是，默认值在定义函数时计算（通
常在加载模块时），因此默认值变成了函数对象的属性。因此，如果默
认值是可变对象，而且修改了它的值，那么后续的函数调用都会受到影
响。
class TwilighBus:
	def __init__(self, passengers=None):
		if passengers is None:
			self.passengers = []
		else:
			self.passengers = list(passengers) #创建参数的副本给实例
			
del和垃圾回收
垃圾回收使用的主要算法是引用计数。实际上，每个对
象都会统计有多少引用指向自己。当引用计数归零时，对象立即就被销
毁：CPython 会在对象上调用 __del__ 方法（如果定义了），然后释放
分配给对象的内存

弱引用
正是因为有引用，对象才会在内存中存在。当对象的引用数量归零后，
垃圾回收程序会把对象销毁。但是，有时需要引用对象，而不让对象存
在的时间超过所需时间。这经常用在缓存中。
弱引用不会增加对象的引用数量。引用的目标对象称为所指对象
（referent）。因此我们说，弱引用不会妨碍所指对象被当作垃圾回收。

>>> import weakref
>>> a_set = {0, 1}
>>> wref = weakref.ref(a_set) ➊
>>> wref
<weakref at 0x100637598; to 'set' at 0x100636748>
>>> wref() ➋
{0, 1}
>>> a_set = {2, 3, 4} ➌
>>> wref() ➍
{0, 1}
>>> wref() is None ➎
False
>>> wref() is None ➏
True
❶ 创建弱引用对象 wref，下一行审查它。
❷ 调用 wref() 返回的是被引用的对象，{0, 1}。因为这是控制台会
话，所以 {0, 1} 会绑定给 _ 变量。
❸ a_set 不再指代 {0, 1} 集合，因此集合的引用数量减少了。但是 _
变量仍然指代它。
❹ 调用 wref() 依旧返回 {0, 1}。
❺ 计算这个表达式时，{0, 1} 存在，因此 wref() 不是 None。但是，
随后 _ 绑定到结果值 False。现在 {0, 1} 没有强引用了。
❻ 因为 {0, 1} 对象不存在了，所以 wref() 返回 None。

WeakValueDictionary 类实现的是一种可变映射，里面的值是对象的
弱引用。被引用的对象在程序中的其他地方被当作垃圾回收后，对应的
键会自动从 WeakValueDictionary 中删除。因
此，WeakValueDictionary 经常用于缓存。

对元组 t 来说，t[:] 不创建副本，而是返回同一个对
象的引用。此外，tuple(t) 获得的也是同一个元组的引用。
>>> t1 = (1, 2, 3)
>>> t2 = tuple(t1)
>>> t2 is t1 ➊
True
>>> t3 = t1[:]
>>> t3 is t1 ➋
True

简单的赋值不创建副本。
对 += 或 *= 所做的增量赋值来说，如果左边的变量绑定的是不可变
对象，会创建新对象；如果是可变对象，会就地修改。
为现有的变量赋予新值，不会修改之前绑定的变量。这叫重新绑
定：现在变量绑定了其他对象。如果变量是之前那个对象的最后一
个引用，对象会被当作垃圾回收。
函数的参数以别名的形式传递，这意味着，函数可能会修改通过参
数传入的可变对象。这一行为无法避免，除非在本地创建副本，或
者使用不可变对象（例如，传入元组，而不传入列表）。
使用可变类型作为函数参数的默认值有危险，因为如果就地修改了
参数，默认值也就变了，这会影响以后使用默认值的调用。

可以在自己的类中定义 __eq__ 方法，决定 == 如何比较
实例。如果不覆盖 __eq__ 方法，那么从 object 继承的方法比较
对象的 ID

解释 Python 中参数传递的方式时，人们经常这样说：“参数按值传
递，但是这里的值是引用。”这么说没错，但是会引起误解，因为
在旧式语言中，最常用的参数传递模式有按值传递（函数得到参数
的副本）和按引用传递（函数得到参数的指针）。在 Python 中，
函数得到参数的副本，但是参数始终是引用。因此，如果参数引用
的是可变对象，那么对象可能会被修改，但是对象的标识不变。此
外，因为函数得到的是参数引用的副本，所以重新绑定对函数外部
没有影响。