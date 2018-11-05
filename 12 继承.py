第十二章

内置类型会忽略字类覆盖的方法
class DoppleDice(dict):
	def __setitem__(self, key, value):
		super.__setitem__(key, [value] * 2)
		
>>> dd = DoppleDice(one=1)
>>> dd
{'one': 1}
# 继承自 dict 的 __init__ 方法显然忽略了我们覆盖的 __setitem__方法：'one' 的值没有重复。
>>> dd['two'] = 2 # [] 运算符会调用我们覆盖的 __setitem__ 方法，按预期那样工作：'two' 对应的是两个重复的值，即 [2, 2]。
>>> dd
{'one': 1, 'two': [2, 2]}
>>> dd.update(three=3) # ➍
>>> dd
{'three': 3, 'one': 1, 'two': [2, 2]}

>>> class AnswerDict(dict):
... def __getitem__(self, key): # ➊
... return 42
...
>>> ad = AnswerDict(a='foo') # ➋
>>> ad['a'] # ➌ 调用了__getitem__方法
42
>>> d = {}
>>> d.update(ad) # ➍dict忽略ad的__getitem__方法
>>> d['a'] # ➎ a的值还是foo
'foo'
>>> d
{'a': 'foo'}

由于内置类型忽略字类的方法覆盖，会出很多问题，此时需要字类化collections.UserDict
>>> import collections
>>>
>>> class DoppelDict2(collections.UserDict):
...     def __setitem__(self, key, value):
...         super().__setitem__(key, [value] * 2)
...
>>> dd = DoppelDict2(one=1)
>>> dd
{'one': [1, 1]}
>>> dd['two'] = 2
>>> dd
{'two': [2, 2], 'one': [1, 1]}
>>> dd.update(three=3)
>>> dd
{'two': [2, 2], 'three': [3, 3], 'one': [1, 1]}
>>>
>>> class AnswerDict2(collections.UserDict):
...    def __getitem__(self, key):
...        return 42
...
>>> ad = AnswerDict2(a='foo')
>>> ad['a']
42
>>> d = {}
>>> d.update(ad)
>>> d['a']
42
>>> d
{'a': 42}

本节所述的问题只发生在 C 语言实现的内置类型内部的方法委托
上，而且只影响直接继承内置类型的用户自定义类。如果子类化使用
Python 编写的类，如 UserDict 或 MutableMapping，就不会受此影
响。

多重继承的顺序

class A:
	def ping(self):
		print('ping', self)

class B(A):
	def pong(self):
		print('pong:', self)
		
class C(A):
	def pong(self):
		print('PONG:', self)
		
class D(B, C):
	def ping(self):
		super().ping()
		print('post-ping:', self)
	def pingpong(self):
		self.ping() # 第一个调用是 self.ping()，运行的是 D 类的 ping 方法，输出这一行和下一行。
		super().ping() #按照__mro__顺序D-B-A，最后调用A的ping方法
		self.pong() #找到B的pong方法
		super().pong() #B的pong
		C.pong(self) #C的pong

>>> from diamond import D
>>> d = D()
>>> d.pingpong()
ping: <diamond.D object at 0x10bf235c0> # ➊
post-ping: <diamond.D object at 0x10bf235c0>
ping: <diamond.D object at 0x10bf235c0> # ➋
pong: <diamond.D object at 0x10bf235c0> # ➌
pong: <diamond.D object at 0x10bf235c0> # ➍
PONG: <diamond.D object at 0x10bf235c0> # ➎

在 D 的实例上调用 d.pong() 方法的话，运行的是哪个 pong 方法呢？
因为B和C都有pong方法
>>> from diamond import *
>>> d = D()
>>> d.pong() # ➊ 直接调用 d.pong() 运行的是 B 类中的版本。
pong: <diamond.D object at 0x10066c278>
>>> C.pong(d) # ➋ 超类中的方法都可以直接调用，此时要把实例作为显式参数传入。
PONG: <diamond.D object at 0x10066c278>
此时查看D类的继承顺序
>>> D.__mro__
(<class 'diamond.D'>, <class 'diamond.B'>, <class 'diamond.C'>,
<class 'diamond.A'>, <class 'object'>)

有时可能需要绕过方法解析顺序，直接
调用某个超类的方法——这样做有时更方便。例如，D.ping 方法可以
这样写：
def ping(self):
	A.ping(self) # 而不是super().ping()
	print('post-ping:', self)
直接在类上调用实例方法时，必须显式传入 self 参数，因为这
样访问的是未绑定方法（unbound method）。



使用super()最为安全
>>> from diamond import D
>>> d = D()
>>> d.ping() # ➊D类的ping方法做了两次调用
ping: <diamond.D object at 0x10cc40630> # ➋第一个调用是super().ping(),super函数按照继承顺序把ping方法委托给了A类
post-ping: <diamond.D object at 0x10cc40630> # ➌第二个调用是输出自身实例
