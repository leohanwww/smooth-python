第十九章

在 Python 中，数据的属性和处理数据的方法统称属性（attribute）。其
实，方法只是可调用的属性。除了这二者之外，我们还可以创建特性
（property），在不改变类接口的前提下，使用存取方法（即读值方法
和设值方法）修改数据属性。
除了特性，Python 还提供了丰富的 API，用于控制属性的访问权限，以
及实现动态属性。使用点号访问属性时（如 obj.attr），Python 解释
器会调用特殊的方法（如 __getattr__ 和 __setattr__）计算属性。
用户自己定义的类可以通过 __getattr__ 方法实现“虚拟属性”，当访
问不存在的属性时（如 obj.no_such_attribute），即时计算属性的
值。

把一个 JSON 数据集转换成一个嵌套着FrozenJSON 对象、列表和简单类型的 FrozenJSON 对象
from collections import abc

class FrozenJSON:
	"""一个只读接口，使用属性访问JSON对象"""
	
	def __init__(self, mapping):
		self.__data = dict(mapping)

	def __getattr__(self, name):
		if hasattr(self.__data, name)
		#如果 name 是实例属性 __data 的属性，返回那个属性。调用 keys等方法就是通过这种方式处理的。
			return getattr(self.__data, name)
		else:
			return FrozenJSON.build(self.__data[name])
			#重新构建一个FrozenJSON
	@classmethod
	def bulid(cls, obj):
		if isinstance(obj, abc.Mapping):
			return cls(obj)#处理映射类型，直接构建
		elif isinstance(obj, abc.MutableSequence):
			#处理列表类型，因为json文件里只有映射和列表这两种
			return [cls.build(item) for item in obj]
		else:
			return obj

>>> from osconfeed import load
>>> raw_feed = load()
>>> feed = FrozenJSON(raw_feed) ➊#构造FrozenJSON类型实例
>>> len(feed.Schedule.speakers) ➋#此时可以用实例的属性访问
357
>>> sorted(feed.Schedule.keys()) ➌
['conferences', 'events', 'speakers', 'venues']
>>> for key, value in sorted(feed.Schedule.items()): ➍
... print('{:3} {}'.format(len(value), key))
...
1 conferences
494 events
357 speakers
53 venues
>>> feed.Schedule.speakers[-1].name ➎
'Carina C. Zona'
>>> talk = feed.Schedule.events[40]
>>> type(talk) ➏
<class 'explore0.FrozenJSON'>
>>> talk.name
'There *Will* Be Bugs'
>>> talk.speakers ➐
[3471, 5199]
>>> talk.flavor ➑
Traceback (most recent call last):
...
KeyError: 'flavor'

处理无效属性名
>>> grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
这里class是系统关键字，不能使用
修改init方法
def __init__(self, mapping):
	self.data = {}
	import keyword
	for key, value in mapping.items():
		if keyword.iskeyword(key):#判断是不是系统关键字
			key += '_' #在后面加上_,变成不是系统关键字可用的
			self.data[key] = value

用于构建实例的__new__
这是一个特殊的类方法，不需用@classmethod
必须返回一个
实例。返回的实例会作为第一个参数（即 self）传给 __init__ 方
法。因为调用 __init__ 方法时要传入实例，而且禁止返回任何值，所
以 __init__ 方法其实是“初始化方法”。真正的构造方法是 __new__。
class FrozenJSON:

	def __new__(cls, arg):
		if isinstance(arg, abc.Mapping):
			return super().__new__(cls)#委托给超类，是object基类的
			#super().__new__(cls) 表达式会调用object.__new__(FrozenJSON)
		elif isinstance(arg, abc.MutableSequence):
			return [cls(item) for item in arg]
		else:
			return arg

	def __init__(self, mapping):
		self.__data = {}
		for key, value in mapping.items():
			if iskeyword(key):
				key += '_'
			self.__data[key] = value

	def __getattr__(self, name):
		if hasattr(self.__data, name):
			return getattr(self.__data, name)
		else:
			return FrozenJSON(self.__data[name])





























