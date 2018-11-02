第十一章

除了抽象基类，每个类都有接口：在类中实现的或者继承的公开的方法或者数据属性，包括特殊方法，如__getitem__，__add__
私有属性不在接口中，但是也能访问，但是最好不要直接访问

接口是实现特定角色的方法集合，如实现了可迭代的方法，实例就可以扮演可迭代对象
一个类可以实现多个接口，从而让它的实例扮演多个角色

序列
class Foo:
	def __getitem__(self, pos):
		return range(0, 30, 10)[pos]

>>>f=Foo()
>>>f[1]
10
>>>for i in f
>>>    print(i)
0
10
20
虽然没有 __iter__ 方法，但是 Foo 实例是可迭代的对象，因为发现有
__getitem__ 方法时，Python 会调用它，传入从 0 开始的整数索引，
尝试迭代对象（这是一种后备机制）。尽管没有实现 __contains__ 方
法，但是 Python 足够智能，能迭代 Foo 实例，因此也能使用 in 运算
符：Python 会做全面检查，看看有没有指定的元素。
综上，鉴于序列协议的重要性，如果没有 __iter__ 和 __contains__
方法，Python 会调用 __getitem__ 方法，设法让迭代和 in 运算符可
用。

使用猴子补丁在运行时实现协议
>>> from random import shuffle
>>> from frenchdeck import FrenchDeck
>>> deck = FrenchDeck()
>>> shuffle(deck)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File ".../python3.3/random.py", line 265, in shuffle
x[i], x[j] = x[j], x[i]
TypeError: 'FrenchDeck' object does not support item assignment
错误消息相当明确，“'FrenchDeck' object does not support item
assignment”（'FrenchDeck' 对象不支持为元素赋值）。这个问题的原因是，shuffle 函数要调换集合中元素的位置，而 FrenchDeck 只实现
了不可变的序列协议。可变的序列还必须提供 __setitem__ 方法。
在运行中设定
>>>def set_card(deck, position, card):
>>>    return self._card[position] = card
>>>FrenchDeck.__setitem__ = set_card #此时让FrenchDeck拥有了__setitem__方法
>>>shuffle(deck) #可以打乱顺序了
>>> deck[:5]
[Card(rank='3', suit='hearts'), Card(rank='4', suit='diamonds'), Card(rank='4',suit='clubs'), Card(rank='7', suit='hearts'), Card(rank='9',suit='spades')]

random.shuffle 函数不关心参数的类型，只要那个对象实现了部
分可变序列协议即可。即便对象一开始没有所需的方法也没关系，后来
再提供也行。

鸭子类型
x和y两个对象都有draw方法，x.draw()和y.draw()
白鹅类型
只要 cls 是抽象基类，即 cls 的元类是
abc.ABCMeta，就可以使用 isinstance(obj, cls)

Python 的抽象基类还有一个重要的实用优势：可以使用 register
类方法在终端用户的代码中把某个类“声明”为一个抽象基类的“虚
拟”子类（为此，被注册的类必须满足抽象基类对方法名称和签名
的要求，最重要的是要满足底层语义契约；但是，开发那个类时不
用了解抽象基类，更不用继承抽象基类）

抽象基类的本质就是几个特殊方法
>>> class Struggle:
... def __len__(self): return 23
...
>>> from collections import abc
>>> isinstance(Struggle(), abc.Sized)
True
无需注册，abc.Sized 也能把 Struggle 识别为自己的
子类，只要实现了特殊方法 __len__ 即可（要使用正确的句法和
语义实现，前者要求没有参数，后者要求返回一个非负整数，指明
对象的长度；如果不使用规定的句法和语义实现特殊方法，如
__len__，会导致非常严重的问题）。
检查是不是序列
isinstance(the_arg, collections.abc.Sequence)

使用鸭子类型处理单个字符串或由字符串组成的可迭代对象
try: 
	field_name = field_name.replace(',' ' ').split() #把对象直接当成字符对象不用事先测试其类型
except AttributeError： #假如不是字符串就没有replace方法
	pass
field_name = tuple(field_name)

从抽象类继承
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck2(collections.MutableSequence): #字类
	ranks = [str(n) for n in range(2, 11)] + list('JQKA')
	suits = 'spades diamonds clubs hearts'.split()
	
	def __init__(self):
		self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
		
	def __len__(self):
		return len(self._cards)
		
	def __getitem__(self, position):
		return self._cards[position]
		
	def __setitem__(self, position, value): #支持洗牌
		self._cards[position] = value
		
	def __delitem__(self, position):
		del self._cards[position]
	# 但是继承 MutableSequence 的类必须实现 __delitem__ 方法，这是 MutableSequence 类的一个抽象方法。
	def insert(self, position, value):
		self._cards.insert(position, value)
	# 此外，还要实现 insert 方法，这是 MutableSequence 类的第三个抽象方法。

colletions.abc 模块中定义了16个抽象基类
Iterable、Container 和 Sized
　　各个集合应该继承这三个抽象基类，或者至少实现兼容的协
议。Iterable 通过 __iter__ 方法支持迭代，Container 通过
__contains__ 方法支持 in 运算符，Sized 通过 __len__ 方法支持
len() 函数。
Sequence、Mapping 和 Set是不可变集合类型
Mappingview：映射方法 .items()、.keys() 和 .values() 返回
的对象分别是 ItemsView、KeysView 和 ValuesView 的实例。

Number
Complex
Real
Rational
Integral
如果想检查一个数是不是整数，可以使用 isinstance(x, numbers.Integral) 这样代码就能接受 int、bool（int 的子类）
如果一个值可能是浮点数类型，可以使用 isinstance(x,numbers.Real) 检查。这样代码就能接受bool、int、float、fractions.Fraction

虚拟字类
from random import randrange
from tombola import Tombola
@Tombola.register # ➊注册为Tombola这个抽象类的虚拟字类
class TomboList(list): # ➋

	def pick(self):
		if self: # ➌
			position = randrange(len(self))
			return self.pop(position) # ➍
		else:
			raise LookupError('pop from empty TomboList')

	load = list.extend
	
	def loaded(self):
		return bool(self) # ➏
		
	def inspect(self):
		return tuple(sorted(self))
注册为虚拟子类的类需要实现虚拟父类的所有方法
>>> from tombola import Tombola
>>> from tombolist import TomboList
>>> issubclass(TomboList, Tombola)
True
>>> t = TomboList(range(100))
>>> isinstance(t, Tombola)
True

类的继承关系在一个特殊的类属性中指定—— __mro__，即方法
解析顺序（Method Resolution Order）。这个属性的作用很简单，按顺序
列出类及其超类，Python 会按照这个顺序搜索方法。 查看
TomboList 类的 __mro__ 属性，你会发现它只列出了“真实的”超类，
即 list 和 object：
>>> TomboList.__mro__
(<class 'tombolist.TomboList'>, <class 'list'>, <class 'object'>)
Tombolist.__mro__ 中没有 Tombola，因此 Tombolist 没有从
Tombola 中继承任何方法。

使用register的方式
可以在定义类的时候直接@class.register
一般这样注册
Sequence.register(tuple)
Sequence.register(str)
Sequence.register(range)
Sequence.register(memoryview)