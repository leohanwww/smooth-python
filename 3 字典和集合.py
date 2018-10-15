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














