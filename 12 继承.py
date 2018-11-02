第十二章

内置类型会忽略字类覆盖的方法
class DoppleDice(dict):
	def __set__item(self, key, value):
		super.__set__item__(key, [value] * 2)
		
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


