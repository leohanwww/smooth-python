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

典型的迭代器模式作用很简单——遍历数据结构

itertools模块提供了很多生成器函数
import itertools
gen = itertools.count(1, .5)
next(gen)不断产出数值
gen = itertools.takewhile(lambda n: n < 3, itertools.count(1, .5))
takewhile生成一个使用另一个
生成器的生成器，给定限定，不会无限产出数值

标注库里的生成器函数
过滤用生成器

itertools	compress(it, selector_it)	并行处理两个可迭代的对象；如果selector_it中的元素是真值，产出 it 中对应的元素
itertools	dropwhile(predicate, it)	和takewhile相反，如果pre产出真值，跳过it中的元素
内置		filter(predicate, it)	过滤器，把it中的元素逐个给predicate(item), 如果产出真值，那么产出it中对应的元素；如果 predicate 是 None，那么只产出真值元素
itertools	filterfalse(predicate, it)	和filter相反，取出不符合predicate条件的it中的值
itertools	islice(it, start, stop, step=1)	产出it的切片，it可以是任何可迭代的对象
itertools	takewhile(predicate, it)	predicate返回真值时产出it里的元素

>>> def vowel(c):
... return c.lower() in 'aeiou'
...
>>> list(filter(vowel, 'Aardvark'))
['A', 'a', 'a']
>>> import itertools
>>> list(itertools.filterfalse(vowel, 'Aardvark'))
['r', 'd', 'v', 'r', 'k']
>>> list(itertools.dropwhile(vowel, 'Aardvark'))
['r', 'd', 'v', 'a', 'r', 'k']
>>> list(itertools.takewhile(vowel, 'Aardvark'))
['A', 'a']
>>> list(itertools.compress('Aardvark', (1,0,1,1,0,1)))
['A', 'r', 'd', 'a']
>>> list(itertools.islice('Aardvark', 4))
['A', 'a', 'r', 'd']
>>> list(itertools.islice('Aardvark', 4, 7))
['v', 'a', 'r']
>>> list(itertools.islice('Aardvark', 1, 7, 2))
['a', 'd', 'a']

用于映射的生成器函数
itertools	accumulate(it, [func])	产出累计的总和，如果有func，把前两个元素传给func，计算结果再把下一个传给func，最后产出结果
内置		enumerate(iterable, start=0)	产出元组，结构是(index, item)
内置		map(func, it1,it2...)		太熟悉了
itertools	startmap(func, it)	把 it 中的各个元素传给 func，产出结果；输入的
可迭代对象应该产出可迭代的元素 iit，然后以func(*iit) 这种形式调用 func

>>> sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
>>> import itertools
>>> list(itertools.accumulate(sample)) # ➊
[5, 9, 11, 19, 26, 32, 35, 35, 44, 45]
>>> list(itertools.accumulate(sample, min)) # ➋
[5, 4, 2, 2, 2, 2, 2, 0, 0, 0]
>>> list(itertools.accumulate(sample, max)) # ➌
[5, 5, 5, 8, 8, 8, 8, 8, 9, 9]
>>> import operator
>>> list(itertools.accumulate(sample, operator.mul)) # ➍
[5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]
>>> list(itertools.accumulate(range(1, 11), operator.mul))
[1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800] # ➎

>>> list(enumerate('albatroz', 1)) # ➊
[(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]
>>> import operator
>>> list(map(operator.mul, range(11), range(11))) # ➋
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
>>> list(map(operator.mul, range(11), [2, 4, 8])) # ➌
[0, 4, 16]
>>> list(map(lambda a, b: (a, b), range(11), [2, 4, 8])) # ➍
[(0, 2), (1, 4), (2, 8)]
>>> import itertools
>>> list(itertools.starmap(operator.mul, enumerate('albatroz', 1))) # ➎
['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']
>>> sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
>>> list(itertools.starmap(lambda a, b: b/a,
... enumerate(itertools.accumulate(sample), 1))) # ➏
[5.0, 4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333,
5.0, 4.375, 4.888888888888889, 4.5]

用于合并的生成器函数
itertools	chain(it1,it2....)	产出无缝链接的所有元素
itertools	chain.from_iterable(it)		假如it里的元素都是可迭代对象，把它们拆开无缝链接在一起
itertools	product(it1,..itN, repeat=1)	计算笛卡尔积，产生N个元素组成的元组
内置		zip(it1,it2...)		组合
itertools	ziplongest(it1,it2...,fillvalue=None)	根据最长的组合，缺少的元素用fillvalue填充

>>> list(itertools.chain('ABC', range(2))) # ➊
['A', 'B', 'C', 0, 1]
>>> list(itertools.chain(enumerate('ABC'))) # ➋
[(0, 'A'), (1, 'B'), (2, 'C')]
>>> list(itertools.chain.from_iterable(enumerate('ABC'))) # ➌
[0, 'A', 1, 'B', 2, 'C']
>>> list(zip('ABC', range(5))) # ➍
[('A', 0), ('B', 1), ('C', 2)]
>>> list(zip('ABC', range(5), [10, 20, 30, 40])) # ➎
[('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]
>>> list(itertools.zip_longest('ABC', range(5))) # ➏
[('A', 0), ('B', 1), ('C', 2), (None, 3), (None, 4)]
>>> list(itertools.zip_longest('ABC', range(5), fillvalue='?')) # ➐
[('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)]

>>> list(itertools.product('ABC', range(2))) # ➊
[('A', 0), ('A', 1), ('B', 0), ('B', 1), ('C', 0), ('C', 1)]
>>> suits = 'spades hearts diamonds clubs'.split()
>>> list(itertools.product('AK', suits)) # ➋
[('A', 'spades'), ('A', 'hearts'), ('A', 'diamonds'), ('A', 'clubs'),
('K', 'spades'), ('K', 'hearts'), ('K', 'diamonds'), ('K', 'clubs')]
>>> list(itertools.product('ABC')) # ➌
[('A',), ('B',), ('C',)]
>>> list(itertools.product('ABC', repeat=2)) # ➍
[('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'),
('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]
>>> list(itertools.product(range(2), repeat=3))
[(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0),
(1, 0, 1), (1, 1, 0), (1, 1, 1)]
>>> rows = itertools.product('AB', range(2), repeat=2)
>>> for row in rows: print(row)
...
('A', 0, 'A', 0)
('A', 0, 'A', 1)
('A', 0, 'B', 0)
('A', 0, 'B', 1)
('A', 1, 'A', 0)
('A', 1, 'A', 1)
('A', 1, 'B', 0)
('A', 1, 'B', 1)
('B', 0, 'A', 0)
('B', 0, 'A', 1)
('B', 0, 'B', 0)
('B', 0, 'B', 1)
('B', 1, 'A', 0)
('B', 1, 'A', 1)
('B', 1, 'B', 0)
('B', 1, 'B', 1)

重新排列的生成器函数
itertools	combinations(it, out_len)	从it产出out_len个元素的组合
itertools	combinations_with_replacement(it, out_len)	从it产出out_len个元素的组合,包括相同元素
itertool	count(start=0, strp=1)	不断产出数字
itertools	cycle(it)	重复不断从it产出元素
itertools	permutations(it, out_len=None)	把 out_len 个 it 产出的元素排列在一起，然后产出这些排列；out_len的默认值等于 len(list(it)
itertools	repeat(item, [times])	重复不断产出指定元素，times指定次数

>>> ct = itertools.count() # ➊
>>> next(ct) # ➋
0 >>> next(ct), next(ct), next(ct) #
➌
(1, 2, 3)
>>> list(itertools.islice(itertools.count(1, .3), 3)) # ➍
[1, 1.3, 1.6]
>>> cy = itertools.cycle('ABC') # ➎
>>> next(cy)
'A'
>>> list(itertools.islice(cy, 7)) # ➏
['B', 'C', 'A', 'B', 'C', 'A', 'B']
>>> rp = itertools.repeat(7) # ➐
>>> next(rp), next(rp)
(7, 7)
>>> list(itertools.repeat(8, 4)) # ➑
[8, 8, 8, 8]
>>> list(map(operator.mul, range(11), itertools.repeat(5))) # ➒
[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

combinations、combinations_with_replacement和 permutations 生成器函数，连同 product函数，称为组合学生成器（combinatoric generator）
>>> list(itertools.combinations('ABC', 2)) # ➊
[('A', 'B'), ('A', 'C'), ('B', 'C')]
>>> list(itertools.combinations_with_replacement('ABC', 2)) # ➋
[('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
>>> list(itertools.permutations('ABC', 2)) # ➌
[('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
>>> list(itertools.product('ABC', repeat=2)) # ➍
[('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'),
('C', 'A'), ('C', 'B'), ('C', 'C')]

重新排列元素的生成器
itertools	groupby(it, key=None)	产出形式为（key，group）的元素，key是分组标准，group 是生成器，用于产出分组里的元素
内置		reversed(seq)	倒序产出seq中的元素
itertools	tee(it, n=2)	产出由N个生成器组成的元组，每个生成器
用于单独产出输入的可迭代对象中的元素，把一个生成器变成N个生成器

>>> list(itertools.groupby('LLLLAAGGG')) # ➊
[('L', <itertools._grouper object at 0x102227cc0>),
('A', <itertools._grouper object at 0x102227b38>),
('G', <itertools._grouper object at 0x102227b70>)]
>>> for char, group in itertools.groupby('LLLLAAAGG'): # ➋
... print(char, '->', list(group))
...
L -> ['L', 'L', 'L', 'L']
A -> ['A', 'A',]
G -> ['G', 'G', 'G']

>>> animals = ['duck', 'eagle', 'rat', 'giraffe', 'bear',
... 'bat', 'dolphin', 'shark', 'lion']
>>> animals.sort(key=len) # ➌
>>> animals
['rat', 'bat', 'duck', 'bear', 'lion', 'eagle', 'shark',
'giraffe', 'dolphin'] #对象要经过排序才能使用groupby
>>> for length, group in itertools.groupby(animals, len): # ➍
... print(length, '->', list(group))
...
3 -> ['rat', 'bat']
4 -> ['duck', 'bear', 'lion']
5 -> ['eagle', 'shark']
7 -> ['giraffe', 'dolphin']

>>> for length, group in itertools.groupby(reversed(animals), len): # ➎
... print(length, '->', list(group))
...
7 -> ['dolphin', 'giraffe']
5 -> ['shark', 'eagle']
4 -> ['lion', 'bear', 'duck']
3 -> ['bat', 'rat']

>>> list(itertools.tee('ABC'))
[<itertools._tee object at 0x10222abc8>, <itertools._tee object at 0x10222ac08
>>> list(itertools.tee('ABC'))
[<itertools._tee object at 0x10222abc8>, <itertools._tee object at 0x10222ac08>]
>>> g1, g2 = itertools.tee('ABC')
>>> next(g1)
'A'
>>> next(g2)
'A'
>>> next(g2)
'B'
>>> list(g1)
['B', 'C']
>>> list(g2)
['C']
>>> list(zip(*itertools.tee('ABC')))
[('A', 'A'), ('B', 'B'), ('C', 'C')]


yield form把不同的生成器结合在一起使用
def chain(*iterables)
	for it in iterables:
		for i in it:
			yield i
>>> s = 'ABC'
>>> t = tuple(range(3))
>>> list(chain(s, t))
['A', 'B', 'C', 0, 1, 2]

def chain(*iterables)
	for it in iterables：
		yield from it
>>> list(chain(s, t))
['A', 'B', 'C', 0, 1, 2]
yield from代替了内层循环


读取迭代器，返回单个值的内置函数
内置		all(it)		it 中的所有元素都为真值时返回 True，否则返回 False；
all([]) 返回 True
内置		any(it)		只要 it 中有元素为真值就返回 True，否则返回 False；
any([]) 返回 False
内置		max(it, key=, default=)		返回 it 中值最大的元素；*key 是排序函数，与 sorted 函数中的一样；如果可迭代的对象为空，返回 default
内置		min(it, key=, default=)		返回 it 中值最小的元素；key 是排序函数，与 sorted 函数中的一样；如果可迭代的对象为空，返回 default
functools	reduce(func, it, [initial])	把前两个元素传给 fun，然后把计算结果和第三个元素传给 func，以此类推，返回最后的结果；如果提供了initial，把它当作第一个元素传入
内置		sum(it, start=0)	it 中所有元素的总和，如果提供可选的 start，会把它加
上（计算浮点数的加法时，可以使用 math.fsum 函数提高精度）
>>> all([1, 2, 3])
True
>>> all([1, 0, 3])
False
>>> all([])
True
>>> any([1, 2, 3])
True
>>> any([1, 0, 3])
True
>>> any([0, 0.0])
False
>>> any([])
False
>>> g = (n for n in [0, 0.0, 7, 8])
>>> any(g)
True
>>> next(g)
8

iter函数的另外用法
迭代对象时会用到iter(x)
另一个用法是传入两个参数，使用常规
的函数或任何可调用的对象创建迭代器。这样使用时，第一个参数必须
是可调用的对象，用于不断调用（没有参数），产出各个值；第二个值
是哨符，这是个标记值，当可调用的对象返回这个值时，触发迭代器抛
出 StopIteration 异常，而不产出哨符。
>>> def d6():
...     return randint(1, 6)
...
>>> d6_iter = iter(d6, 1)
>>> d6_iter
<callable_iterator object at 0x00000000029BE6A0>
>>> for roll in d6_iter:
...     print(roll)
...
4
3
6
3
掷筛子直到抛出1，这时抛出StopIteration

这段代码逐行读取文件，直到遇到空行或者到达文件末尾为止：
with open('data.txt') as fp:
	for line in iter(fp, '\n')
		process_line(line)

把生成器当成协程
与 .__next__() 方法一样，.send() 方法致使生成器前进到下一个
yield 语句。不过，.send() 方法还允许使用生成器的客户把数据发给
自己，即不管传给 .send() 方法什么参数，那个参数都会成为生成器
函数定义体中对应的 yield 表达式的值。也就是说，.send() 方法允
许在客户代码和生成器之间双向交换数据。而 .__next__() 方法只允
许客户从生成器中获取数据。
像这样使用的话，生成器就变身为协程

协程的例子
def printer():
	counter = 0
	while True:
		string = (yield)
		print('{0}, {1}'.format(count, string))
		count += 1

if __name__ == '__main__':
	p = printer()
	next(p)
	p.send('Hi')
	p.send('my name is...')
	p.send('leo')

0 Hi
1 My name is...
2 leo
子程序处理到yield时挂起并返回主程序，主程序通过send唤起子程序并传入数据，以此交替进行

生成器用于生成供迭代的数据
协程是数据的消费者，虽然在协程中会使用 yield 产出值，但这与迭代无关




