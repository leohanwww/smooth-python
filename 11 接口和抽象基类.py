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

