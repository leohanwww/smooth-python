第十三章

重载运算符可以让用户重新定义中缀运算符如+ | - ~等
函数调用() 属性访问. 元素访问切片[]也是运算符

- __neg__ 取负运算符
+ __pos__ 取正运算符
~ __invert__ 对整数按位取反

def __abs__(self):
	return math.sqrt(sum(x * x for x in self))
def __neg__(self):
	return Vector(-x for x in self) ➊#取反
def __pos__(self):
	return Vector(self) ➋ #一个全新的

重载向量加法运算符+
def __add__(self, other):
	pairs = itertools.zip_longest(self, other, fillvalue=0.0)
	return Vector(a + b for a, b in pairs)
但是如果other在左边，就会出错，这是因为调用了Vector的a.__add__(b)方法
如果a没有__add__方法，就检查b有没有__radd__方法，如果有，就调用b的__radd__方法
b.__radd__(a)

def __radd__(self, other): # ➋直接委托给__add__
	return self + other #此时我认为+号已经被__add__重载了

如果由于类型不兼容而导致运算符特殊方法无法返回有效的结果，那么应该返
回 NotImplemented，而不是抛出 TypeError。返回 NotImplemented
时，另一个操作数所属的类型还有机会执行运算，即 Python 会尝试调用
反向方法。
def __add__(self, other):
	try:
		pairs = itertools.zip_longest(self, other, fillvalue=0.0)
		return Vector(a + b for a, b in pairs)
	except TypeError:
		return NotImplemented
def __radd__(self, other):
	return self + other
	

重载标量乘法*
def __mul__(self, scalar):
	return Vector(n * scalar for n in self)
def __rmul__(self, scalar):
	return self * scalar

运算符正向方法反向方法就地方法说明
+ __add__ __radd__ __iadd__ 加法或拼接
- __sub__ __rsub__ __isub__ 减法
* __mul__ __rmul__ __imul__ 乘法或重复复制
/ __truediv__ __rtruediv__ __itruediv__ 除法
// __floordiv__ __rfloordiv__ __ifloordiv__ 整除
% __mod__ __rmod__ __imod__ 取模
divmod() __divmod__ __rdivmod__ __idivmod__返回由整除的商和模数组成的元组
** pow() __pow__ __rpow__ __ipow__ 取幂*
@ __matmul__ __rmatmul__ __imatmul__ 矩阵乘法#
& __and__ __rand__ __iand__ 位与
| __or__ __ror__ __ior__ 位或
^ __xor__ __rxor__ __ixor__ 位异或
<< __lshift__ __rlshift__ __ilshift__ 按位左移
>> __rshift__ __rrshift__ __irshift__ 按位右移

比较运算符
                                   失败处理
a == b a.__eq__(b) b.__eq__(a) 返回 id(a) == id(b)
a != b a.__ne__(b) b.__ne__(a) 返回 not (a == b)
a > b a.__gt__(b) b.__lt__(a) 抛出 TypeError
a < b a.__lt__(b) b.__gt__(a) 抛出 TypeError
a >= b a.__ge__(b) b.__le__(a) 抛出 TypeError
a <= b a.__le__(b) b.__ge__(a) 抛出TypeError

增量赋值+= -=
增量赋值不会修改不可变目标，而是新建实例，然后重新绑定
如果没有实现就地运算符__iadd__，增量运算符只是语法糖，a += b和a = a + b一样
如果只定义__add__，+=一样能使用

def __add__(self, other): #正向运算符
	if isinstance(other, Tombola): #判断类型是否一致
		return AddableBingoCage(self.inspect() + other.inspect())
	else：
		return NotImplemented
def __iadd__(self, other):#就地运算符
	if isinstance(other, Tombola):
		other_iterable = other.inspect() #构建新的可迭代
	else:
		try:
			other_iterable = iter(other)
		except TypeError:
			self_cls = type(self).__name__
			msg = "right operand in += must be {!r} or an iterable"
			raise TypeError(msg.format(self_cls))
	self.load(other_iterable)
	return self
	
一般来说，如果中缀运算符的正向方法（如 __mul__）只处
理与 self 属于同一类型的操作数，那就无需实现对应的反向方法
（如 __rmul__），因为按照定义，反向方法是为了处理类型不同
的操作数。

如果选择使用 isinstance，要小
心，不能测试具体类，而要测试 numbers.Real 抽象基类，例如
isinstance(scalar, numbers.Real)。
