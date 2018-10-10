第一章 python数据模型

理解python的一致性
数据模型其实是对python框架的描述，它规范了自身构建模块的接口
如obj[key]背后调用的是__getitem__方法
可以自建数据模型并实现一些特殊方法来提升模型的可扩展性，如创建__len__ 方法后，就能使用len(obj)

这些特殊方法名能让你自己的对象实现和支持以下的语言构架，并与之交互：
迭代
集合类
属性访问
运算符重载
函数和方法的调用
对象的创建和销毁
字符串表示形式和格式化
管理上下文（即 with 块）

特殊方法，魔术方法(magic method)，也都是双下符表示的，也叫双下方法__getitem__


具名元组nemedtuple，用以创建只有属性而没有方法的类，其实就是一个简单的类
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])
new_card = Card('5', 'heart')

class FrenchDeck:
    ranks = [2,3,4,5,6,7,8,9,10,J,Q,K,A]
    suits = 'spades diamonds clubs hearts'.split()
	
    def __init__(self):
        self.__cards = [Card(rank, suit) for suit in self.suits
                                         for rank in self.ranks]
										
    def __len__(self): 
        return len(self.__cards)
		
    def __getitem__(self, position):
        return self.__cards[position]
		
deck = Frenchdeck()
len(deck) 利用__len__方法
deck[0] 利用__getitem__方法使Card变成可迭代 deck[:3] deck[12::13]每隔13张拿牌
还能加入__setitem__(self, rank, suit)方法使洗牌变为可能


通过内置方法调用特殊方法 如 len iter str


from math import hypot

calss Vector:
	
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		
	'''控制台调用返回的字符,用%r表示用repr的形式，能够重现所代表的对象
	    题外话：如果没定义__str__ 系统会默认用__repr__代替'''	
	def __repr__(self):
		return 'Vector (%r, %r)' % (self.x, self.y)
	
	def __abs__(self):
		return hypot(self.x, self.y)
	
	'''通过 __add__ 和 __mul__，示例 1-2 为向量类带来了 + 和 * 这两个算术运算符
	这两个方法的返回值都是新创建的向量对象，被操作的两个向量（self 或 other）还是原封不动，
	代码里只是读取了它们的值而已。中缀运算符的基本原则就是不改变操作对象，而是产出一个新的值'''
	def __add__(self, other):
		x = self.x + other.x
		y = self.y + other.y
		return Vector(x, y)
	
	def __mul__(self, num):
		return Vector(self.x * num, self.y * num)
	
	def __bool__(self):
		return bool(abs(self))
		
		


		
特殊方法
1.字符串、序列方法
__repr__ __str__ __format__ __bytes__
2.数值转换
__abs__ __bool__ __complex__ __int__ __float__ __hash__ __index__
3.集合模拟
__len__ __getitem__ __setitem__ __contains__
4.迭代枚举
__iter__ __reversed__ __next__
5.可调用
__call__
6.上下文管理
__enter__ __exit__
7.实例创建和销毁
__new__ __init__ __del__
8.属性管理
__getattr__ __setattr__ __delattr__ __getattribute__ __dir__
9.属性描述符
__get__ __set__ __delete__
10.类服务
__prepare__ __instancecheck__ __subclasscheck__


类
别
方法名和对应的运算符
一
元
运
算
符
__neg__ -、__pos__ +、__abs__ abs()
众
多
比
较
运
算
符
__lt__ <、__le__ <=、__eq__ ==、__ne__ !=、__gt__ >、__ge__ >=
算
术
运
算
符
__add__ +、__sub__ -、__mul__ *、__truediv__ /、__floordiv__ //、__mod__ %、__divmod__
divmod()、__pow__ ** 或pow()、__round__ round()
反
向
算
术
运
算
符
__radd__、__rsub__、__rmul__、__rtruediv__、__rfloordiv__、__rmod__、__rdivmod__、__rpow__
增
量
赋
值
算
术
运
算
符
__iadd__、__isub__、__imul__、__itruediv__、__ifloordiv__、__imod__、__ipow__
位
运
算
符
__invert__ ~、__lshift__ <<、__rshift__ >>、__and__ &、__or__ |、__xor__ ^
反
向
位
运
算
符
__rlshift__、__rrshift__、__rand__、__rxor__、__ror__
增
量
赋
值
位
运
算
符
__ilshift__、__irshift__、__iand__、__ixor__、__ior__

len 之所以不是一个普通方法，是为了让 Python 自带的数据
结构可以走后门，abs 也是同理。但是多亏了它是特殊方法，我们也可
以把 len 用于自定义数据类型。你只要在自定义的类中定义__len__这个方法，
就能把len作用于你自己创建的类型

