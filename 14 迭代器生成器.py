第十四章

所有生成器都是迭代器，因为生成器完全实现了迭代器接口
迭代器用于从集合中取出元素；而生成器用于“凭空”生成元素

import re
import repllib

RE_WORD = re.compile('\w+')

class Sentence:

	def __init__(self, text):
		self.text = text
		self.words = RE_WORD.findall(text)
		
	def __getitem__(self, index):
		return self.words[index]
		
	def __len__(self):
		return len(self.words)
		
	def __repr__(self):
		return 'Sentence(%s)' % repllib.repr(self.text)
		
序列可以迭代的原因：iter函数
解释器需要迭代对象 x 时，会自动调用 iter(x)。
有iter方法，就调用，没有的话，就调用getitem
检查对象 x 能否迭代，最准确的方法是：
调用 iter(x) 函数，如果不可迭代，再处理 TypeError 异常

迭代器
我们要明确可迭代的对象和迭代器之间的关系：Python 从可迭代的对象
中获取迭代器。
标准的迭代器有两个方法 __next__, __iter__
for a in b 背后调用了迭代器iter(b)

检查对象 x 是否为迭代器最好的方式是调用
isinstance(x, abc.Iterator)。得益于
Iterator.__subclasshook__ 方法，即使对象 x 所属的类不是
Iterator 类的真实子类或虚拟子类，也能这样检查。

典型迭代器
class Sentence: #可迭代对象
	.....
	def __iter__(self):
		return SentenceIterator(self.words)
	#根据可迭代协议，__iter__ 方法实例化并返回一个迭代器。

class SentenceIterator: #迭代器
	def __init__(self, words):
		self.words = words
		self.index = 0
	def __next__(self): #迭代器要有此方法
		try:
			word = self.words[self.index] ➎#取出元素
		except IndexError:
			raise StopIteration() ➏
		self.index += 1 ➐
		return word ➑
	def __iter__(self): #迭代器也要有此方法
		return self
#这个方法臃肿而繁琐，要实现可迭代对象还要为之写一个或者几个专门的迭代器
可迭代的对象有个 __iter__ 方法，每次都实例化一个新的迭代器
而迭代器要实现 __next__ 方法，返回单个元素，此外还要实现
__iter__ 方法，返回迭代器本身。

可迭代的对象一定不能是自身的迭代器。也就是说，可迭代的对象
必须实现 __iter__ 方法，但不能实现 __next__ 方法。
另一方面，迭代器应该一直可以迭代。迭代器的 __iter__ 方法应
该返回自身。

符合python风格的生成器函数
class Sentence:
	...
	def __iter__(self):
		for word in self.words
			yield word
		return #这个 return 语句不是必要的；这个函数可以直接“落空”，自动返回。不管有没有 return 语句，生成器函数都不会抛出 StopIteration异常，而是在生成完全部值之后会直接退出。
这里迭代器其实是生成器对象，每次调用 __iter__ 方法都会
自动创建，因为这里的 __iter__ 方法是生成器函数。

生成器函数的工作原理
只要 Python 函数的定义体中有 yield 关键字，该函数就是生成器函
数。调用生成器函数时，会返回一个生成器对象。也就是说，生成器函
数是生成器工厂。
　普通的函数与生成器函数在句法上唯一的区别是，在后者的
定义体中有 yield 关键字

>>> def gen_123(): # ➊
... yield 1 # ➋
... yield 2
7
7
8
8
... yield 3
...
>>> gen_123 # doctest: +ELLIPSIS
<function gen_123 at 0x...> # ➌ 函数对象
>>> gen_123() # doctest: +ELLIPSIS
<generator object gen_123 at 0x...> # ➍ 调用函数对象时产生生成器
>>> for i in gen_123(): # ➎
... print(i)
1
2
3
>>> g = gen_123() #
>>> next(g) # ➐
1 >>> next(g)
2 >>> next(g)
3 >>> next(g) #
➑
Traceback (most recent call last):
...
StopIteration
# 生成器函数不会抛出StopIteration,但是生成器会抛出StopIteration

惰性实现
为了节省内存，在init阶段不构建self.words列表
class Sentence：
	def __init__(self, text):
		self.text = text
	def __repr__(self):
		return 'Sentence(%s)' % repllib.repr(self.text)
	def __iter__(self):
		for match in RE_WORD.finditer(self.text):
			yield match.group()
	
生成器表达式
生成器表达式可以理解为列表推导的惰性版本：不会迫切地构建列表，
而是返回一个生成器，按需惰性生成元素。也就是说，如果列表推导是
制造列表的工厂，那么生成器表达式就是制造生成器的工厂。
def __iter__(self):
	return (match.group() for match in RE_WORD.finditer(self.text))
#这里不是生成器函数了，变成了生成器表达式
#调用__iter__方法会得到一个生成器对象