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