第三章 字典和集合

标准库里的所有映射类型都是利用 dict 来实现的，因此它们有个共同
的限制，即只有可散列的数据类型才能用作这些映射里的键（只有键有
这个要求，值并不需要是可散列的数据类型）。
什么是可散列的数据类型
如果一个对象是可散列的，那么在这个对象的生命周期中，它
的散列值是不变的，而且这个对象需要实现 __hash__() 方
法。另外可散列对象还要有 __eq__() 方法，这样才能跟其他
键做比较。如果两个可散列对象是相等的，那么它们的散列值
一定是一样的……
原子不可变数据类型（str、bytes 和数值类型）都是可散列类
型，frozenset 也是可散列的，因为根据其定义，frozenset 里
只能容纳可散列类型。元组的话，只有当一个元组包含的所有元素
都是可散列类型的情况下，它才是可散列的。来看下面的元组
tt、tl 和 tf：
>>> tt = (1, 2, (30, 40))
>>> hash(tt)
8027212646858338501
>>> tl = (1, 2, [30, 40])
>>> hash(tl)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> tf = (1, 2, frozenset([30, 40]))
>>> hash(tf)
-4118419923444501110
一般来讲用户自定义的类型的对象都是可散列的，散列值就是它们
的 id() 函数的返回值，所以所有这些对象在比较的时候都是不相
等的。如果一个对象实现了 __eq__ 方法，并且在方法中用到了这
个对象的内部状态的话，那么只有当所有这些内部状态都是不可变
的情况下，这个对象才是可散列的。
字典的几种构造方法
>>> a = dict(one=1, two=2, three=3)
>>> b = {'one': 1, 'two': 2, 'three': 3}
>>> c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
>>> d = dict([('two', 2), ('one', 1), ('three', 3)])
>>> e = dict({'three': 3, 'one': 1, 'two': 2})
>>> a == b == c == d == e
True

字典推导
>>> DIAL_CODES = [ ➊
... (86, 'China'),
... (91, 'India'),
... (1, 'United States'),
... (62, 'Indonesia'),
... (55, 'Brazil'),
... (92, 'Pakistan'),
... (880, 'Bangladesh'),
... (234, 'Nigeria'),
... (7, 'Russia'),
... (81, 'Japan'),
... ]
>>> country_code = {country: code for code, country in DIAL_CODES} ➋
>>> country_code
{'China': 86, 'India': 91, 'Bangladesh': 880, 'United States': 1,
'Pakistan': 92, 'Japan': 81, 'Russia': 7, 'Brazil': 55, 'Nigeria':
234, 'Indonesia': 62}
>>> {code: country.upper() for country, code in country_code.items() 从已经是字典里的items提取
... if code < 66}
{1: 'UNITED STATES', 55: 'BRAZIL', 62: 'INDONESIA', 7: 'RUSSIA'}

常见映射方法

dict 
collections.defaultdict 
collections.OrdereDict

d.setdefault(k,[default]) 若字典里有键k，则把它对应的值设置为 default，然后返回这个值；若无，则让 d[k] = default，然后返回 default
>>> d_ne.setdefault('k', [99,])
[99]
>>> d_ne
{'s': [1], 'd': [1], 'j': [1], 'i': [1], 'h': [1], 'r': [1], 'm': [1], 'c': [1], 'k': [99]}

>>> d_ne['b'] = 88 #调用d_ne.__setitem__()
>>> d_ne
{'s': 66, 'd': [1], 'j': [1], 'i': [1], 'h': [1], 'r': [1], 'm': [1], 'c': [1], 'k': [99], 'tt': 55, 'b': 88}

映射的弹性键查询
有时候为了方便起见，就算某个键在映射里不存在，我们也希望在通过
这个键读取值的时候能得到一个默认值。有两个途径能帮我们达到这个
目的，一个是通过 defaultdict 这个类型而不是普通的 dict，另一个
是给自己定义一个 dict 的子类，然后在子类中实现 __missing__ 方
法。
defaultdict：处理找不到的键的一个选择

特殊方法__missing__
__missing__ 方法只会被 __getitem__ 调用（比如在表达
式 d[k] 中）提供 __missing__ 方法对 get 或者
__contains__（in 运算符会用到这个方法）这些方法的使用没有
影响
示例 3-7　StrKeyDict0 在查询的时候把非字符串的键转换为字符
串
class StrKeyDict0(dict): ➊

    def __missing__(self, key):
        if isinstance(key, str): ➋
            raise KeyError(key)
    return self[str(key)] ➌ #把非字符变成字符以便继续查找
		
    def get(self, key, default=None):
        try:
            return self[key] ➍
    except KeyError:
        return default ➎
		
    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys() ➏
❶ StrKeyDict0 继承了 dict。
❷ 如果找不到的键本身就是字符串，那就抛出 KeyError 异常。
❸ 如果找不到的键不是字符串，那么把它转换成字符串再进行查找。
❹ get 方法把查找工作用 self[key] 的形式委托给 __getitem__，这
样在宣布查找失败之前，还能通过 __missing__ 再给某个键一个机
会。
❺ 如果抛出 KeyError，那么说明 __missing__ 也失败了，于是返回
default。
❻ 先按照传入键的原本的值来查找（我们的映射类型中可能含有非字
符串的键），如果没找到，再用 str() 方法把键转换成字符串再查找
一次。
下面来看看为什么 isinstance(key, str) 测试在上面的
__missing__ 中是必需的。
如果没有这个测试，只要 str(k) 返回的是一个存在的键，那么
__missing__ 方法是没问题的，不管是字符串键还是非字符串键，它
都能正常运行。但是如果 str(k) 不是一个存在的键，代码就会陷入无
限递归。这是因为 __missing__ 的最后一行中的 self[str(key)] 会
调用 __getitem__，而这个 str(key) 又不存在，于是 __missing__
又会被调用。

字典变种

collections.OrderedDict
　　这个类型在添加键的时候会保持顺序，因此键的迭代次序总是一致
的。OrderedDict 的 popitem 方法默认删除并返回的是字典里的最后
一个元素，
import collections
d = collections.OrderedDict()

collections.Counter
　　这个映射类型会给键准备一个整数计数器。每次更新一个键的时候
都会增加这个计数器。所以这个类型可以用来给可散列表对象计数，或
者是当成多重集来用——多重集合就是集合里的元素可以出现不止一
次。Counter 实现了 + 和 - 运算符用来合并记录，还有像
most_common([n]) 这类很有用的方法。most_common([n]) 会按照次
序返回映射里最常见的 n 个键和它们的计数
 |  >>> c = Counter('abcdeabcdabcaba')  # count elements from a string
 |
 |  >>> c.most_common(3)                # three most common elements
 |  [('a', 5), ('b', 4), ('c', 3)]
 |  >>> sorted(c)                       # list all unique elements
 |  ['a', 'b', 'c', 'd', 'e']
 |  >>> c.update('aaaa')                # insert into c 
 |  >>> c.most_common(3)
 |  >>> [('a', 8), ('b', 4), ('c', 3)]
 
colllections.UserDict
　　这个类其实就是把标准 dict 用纯 Python 又实现了一遍。

子类化UserDict
就创造自定义映射类型来说，以 UserDict 为基类，总比以普通的
dict 为基类要来得方便。
UserDict 有一个叫作 data 的属性，是 dict 的实例，这个属性实际上
是 UserDict 最终存储数据的地方。

示例 3-8　无论是添加、更新还是查询操作，StrKeyDict 都会把
非字符串的键转换为字符串
import collections
class StrKeyDict(collections.UserDict): ➊
	def __missing__(self, key): ➋
		if isinstance(key, str):
		raise KeyError(key)
	return self[str(key)]
	
	def __contains__(self, key):
		return str(key) in self.data ➌
		
	def __setitem__(self, key, item):
		self.data[str(key)] = item ➍
		
❶ StrKeyDict 是对 UserDict 的扩展。
❷ __missing__ 跟示例 3-7 里的一模一样。
❸ __contains__ 则更简洁些。这里可以放心假设所有已经存储的键都
是字符串。因此，只要在 self.data 上查询就好了，并不需要像
StrKeyDict0 那样去麻烦 self.keys()。
❹ __setitem__ 会把所有的键都转换成字符串。由于把具体的实现委
托给了 self.data 属性，这个方法写起来也不难。


不可变映射

　用 MappingProxyType 来获取字典的只读实例
mappingproxy
>>> from types import MappingProxyType
>>> d = {'A':99}
>>> d_proxy = MappingProxyType(d)
>>> d_proxy
>>> mappingproxy({'A': 99})
d_proxy 是动态的，也就是说对 d 所做的任何改动都会反馈到它上
面。

集合论

集合的本质是许多唯一对象的聚集。因此，集合可以用于去重
集合中的元素必须是可散列的，set 类型本身是不可散列的，但是
frozenset 可以。因此可以创建一个包含不同 frozenset 的 set。

集合可进行 a | b 合集 a & b 交集 a - b 差集
needles & haystack 求两集的相同元素
set(needles) & set(haystack) 用在任意可迭代对象上

集合的表达式
>>> s = {1} #有内容的集合用{}
>>> type(s)
<class 'set'>
>>> s
{1}
>>> s.pop()
1 >>> s
set() #空集的表达式
frozenset()没有特殊语句，只能用构造方法创建 frozenset(range(10))

集合推导式同字典推导和列表推导式
{chr(i) for i in range(32, 256)}

集合的操作

set.remove(obj)和set.discard(obj)的区别在于，当obj存在于set中时，都将其删除；但当obj不存在于set中时，remove()会报错，discard()不会。


dict和背后的散列表
dict的背后是散列表，是一种稀疏数组，里面的单元叫做表元，在dict的散列表当中，每个键值对都占用一个表元，每个表元都有两
个部分，一个是对键的引用，另一个是对值的引用。因为 Python 会设法保证大概还有三分之一的表元是空的，所以在快要达
到这个阈值的时候，原有的散列表会被复制到一个更大的空间里面。如果要把一个对象放入散列表，那么首先要计算这个元素键的散列值。hash()
散列表算法
为了获取 my_dict[search_key] 背后的值，Python 首先会调用
hash(search_key) 来计算 search_key 的散列值，把这个值最低
的几位数字当作偏移量，在散列表里查找表元（具体取几位，得看
当前散列表的大小）。若找到的表元是空的，则抛出 KeyError 异
常。若不是空的，则表元里会有一对 found_key:found_value。
这时候 Python 会检验 search_key == found_key 是否为真，如
果它们相等的话，就会返回 found_value。
如果 search_key 和 found_key 不匹配的话，这种情况称为散列
冲突。发生这种情况是因为，散列表所做的其实是把随机的元素映
射到只有几位的数字上，而散列表本身的索引又只依赖于这个数字
的一部分。为了解决散列冲突，算法会在散列值中另外再取几位，
然后用特殊的方法处理一下，把新得到的数字再当作索引来寻找表
元。 若这次找到的表元是空的，则同样抛出 KeyError；若非
空，或者键匹配，则返回这个值；或者又发现了散列冲突，则重复
以上的步骤。

dict的实现
键必须是可散列对象
一个可散列的对象必须满足以下要求。
(1) 支持 hash() 函数，并且通过 __hash__() 方法所得到的散列
值是不变的。
(2) 支持通过 __eq__() 方法来检测相等性。
(3) 若 a == b 为真，则 hash(a) == hash(b) 也为真。
所有由用户自定义的对象默认都是可散列的，因为它们的散列值由
id() 来获取，而且它们都是不相等的。
字典在内存上的开销巨大
键查询很快
键的次序取决于添加顺序
往字典里添加新键可能会改变已有键的顺序
不要对字典同时进行迭代和修改。如果想扫描并修改一
个字典，最好分成两步来进行：首先对字典迭代，以得出需要添加
的内容，把这些内容放在一个新字典里；迭代结束之后再对原有字
典进行更新。

set的实现和frozenset
set 和 frozenset 的实现也依赖散列表，但在它们的散列表里存放的
只有元素的引用（就像在字典里只存放键而没有相应的值
