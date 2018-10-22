第七章

#装饰器可以改变或者不改变函数的作用，这要看装饰器是不是返回函数本身
def deco(func):
    print('running %s' % func.__name__)
    return func

@deco
def to_decod():
    print('func is running...')
    
to_decod()

>>> running to_decod
>>> func is running...

综上，装饰器的一大特性是，能把被装饰的函数替换成其他函数。第二
个特性是，装饰器在加载模块时立即执行

registry = [] ➊
def register(func): ➋
	print('running register(%s)' % func) ➌
	registry.append(func) ➍
	return func ➎
	
@register ➏
def f1():
	print('running f1()')
	
@register
def f2():
	print('running f2()')
	
def f3(): ➐
	print('running f3()')
	
def main(): ➑
	print('running main()')
	print('registry ->', registry)
	f1()
	f2()
	f3()
if __name__=='__main__':
	main() ➒
	
$ python3 registration.py
running register(<function f1 at 0x100631bf8>)
running register(<function f2 at 0x100631c80>)
running main()
registry -> [<function f1 at 0x100631bf8>, <function f2 at 0x100631c80>]
running f1()
running f2()
running f3()
，register 在模块中其他函数之前运行（两次）。调用
register 时，传给它的参数是被装饰的函数，例如 <function f1 at
0x100631bf8>。
如果导入 registration.py 模块（不作为脚本运行），输出如下：
>>> import registration
running register(<function f1 at 0x10063b1e0>)
running register(<function f2 at 0x10063b268>)
此时查看 registry 的值，得到的输出如下：
>>> registration.registry
[<function f1 at 0x10063b1e0>, <function f2 at 0x10063b268>]

实际情况是，装饰器通常在一个模块中定义，然后应用到其他模块中的函数上。
register 装饰器返回的函数与通过参数传入的相同。实际上，大
多数装饰器会在内部定义一个函数，然后将其返回。

改进优惠策略
promos = [] ➊
def promotion(promo_func): ➋
	promos.append(promo_func)
	return promo_func

@promotion ➌
def fidelity(order):
	"""为积分为1000或以上的顾客提供5%折扣"""
	return order.total() * .05 if order.customer.fidelity >= 1000 else 0

@promotion
def bulk_item(order):
	"""单个商品为20个或以上时提供10%折扣"""
	discount = 0
	for item in order.cart:
		if item.quantity >= 20:
			discount += item.total() * .1
	return discount

@promotion
def large_order(order):
	"""订单中的不同商品达到10个或以上时提供7%折扣"""
	distinct_items = {item.product for item in order.cart}
	if len(distinct_items) >= 10:
	return order.total() * .07
	return 0

def best_promo(order): ➍
	"""选择可用的最佳折扣"""
	return max(promo(order) for promo in promos)
	
❶ promos 列表起初是空的。
❷ promotion 把 promo_func 添加到 promos 列表中，然后原封不动
地将其返回。
❸ 被 @promotion 装饰的函数都会添加到 promos 列表中。
❹ best_promos 无需修改，因为它依赖 promos 列表。

全局变量
如果在函数中赋值时想让解释器把 b 当成全局变量，要使用 global 声
明：
>>> b = 6
>>> def f3(a):
... global b
... print(a)
... print(b)
... b = 9
...
>>> f3(3)
3
6 
>>> b
9
>>> f3(3)
3
9 
>>> b = 30
>>> b

闭包

def make_averager():
	series = []
	#闭包开始
	def averager(new_value):
		series.append(new_value) #series是自由变量
		total = sum(series)
	return total/len(series)
	#闭包结束
	return averager
averager 的闭包延伸到那个函数的作用域之外，包含自由
变量 series 的绑定
>>> avg = make_averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
闭包是一种函数，它会保留定义函数时存在的自由变量的绑定，
这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定。
注意，只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中
的外部变量。

nonlocal声明

def make_averager():
	count = 0
	total = 0
	
	def averager(new_value):
		count += 1
		total += new_value
		return total / count
		
	return averager
	
>>> avg = make_averager()
>>> avg(10)
Traceback (most recent call last):
...
UnboundLocalError: local variable 'count' referenced before assignment
在 averager 的定义
体中为 count 赋值了，这会把 count 变成局部变量
示例 7-9 没遇到这个问题，因为我们没有给 series 赋值，我们只是调
用 series.append，并把它传给 sum 和 len。也就是说，我们利用了
列表是可变的对象这一事实。
但是对数字、字符串、元组等不可变类型来说，只能读取，不能更新。
如果尝试重新绑定，例如 count = count + 1，其实会隐式创建局部
变量 count。这样，count 就不是自由变量了，因此不会保存在闭包
中。
　计算移动平均值，不保存所有历史
def make_averager():
	count = 0
	total = 0

	def averager(new_value):
		nonlocal count, total
		count += 1
		total += new_value
		return total / count
		
	return averager

简单装饰器
import time
def clock(func): #，factorial 会作为 func 参数传给 clock
	def clocked(*args)
		t0 = time.perf_counter()
		result = func(*args)
		elapsed = time.perf_counter() - t0
		name = func.__name__
		arg_str = ','.join(repr(arg) for arg in args)
		print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
		return result
	
	return clocked #clock 函数会返回 clocked 函数，Python 解释器在背后会把 clocked 赋值给 factorial。

import time
from clockdeco import clock

@clock
def snooze(seconds):
	time.sleep(seconds)
	
@clock
def factorial(n):
	return 1 if n < 2 else n * factorial(n - 1)
	
if __name__=='__main__':
	print('*' * 40, 'Calling snooze(.123)')
	snooze(.123)
	print('*' * 40, 'Calling factorial(6)')
	print('6! =', factorial(6))
	
$ python3 clockdeco_demo.py
**************************************** Calling snooze(123)
[0.12405610s] snooze(.123) -> None
**************************************** Calling factorial(6)
[0.00000191s] factorial(1) -> 1
[0.00004911s] factorial(2) -> 2
[0.00008488s] factorial(3) -> 6
[0.00013208s] factorial(4) -> 24
[0.00019193s] factorial(5) -> 120
[0.00026107s] factorial(6) -> 720
6! = 720
这是装饰器的典型行为：把被装饰的函数替换成新函数，二者接受相同
的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做些
额外操作。

标准库中的两个装饰器
使用functools.lru_cache做备忘
lru_cache保存耗时的函数结果，避免重复计算
import functools
from clockdeco import clock

@functools.lru_cache() # ➊
@clock # ➋
def fibonacci(n):
	if n < 2:
		return n
	return fibonacci(n-2) + fibonacci(n-1)
	
if __name__=='__main__':
	print(fibonacci(6))

❶ 注意，必须像常规函数那样调用 lru_cache。这一行中有一对括
号：@functools.lru_cache()。这么做的原因是，lru_cache 可以
接受配置参数，稍后说明。
❷ 这里叠放了装饰器：@lru_cache() 应用到 @clock 返回的函数上。

$ python3 fibo_demo_lru.py
[0.00000119s] fibonacci(0) -> 0
[0.00000119s] fibonacci(1) -> 1
[0.00010800s] fibonacci(2) -> 1
[0.00000787s] fibonacci(3) -> 2
[0.00016093s] fibonacci(4) -> 3
[0.00001216s] fibonacci(5) -> 5
[0.00025296s] fibonacci(6) -> 8

functools.lru_cache(maxsize=128, typed=False)
maxsize 参数指定存储多少个调用的结果。缓存满了之后，旧的结果会
被扔掉，腾出空间。为了得到最佳性能，maxsize 应该设为 2 的
幂。typed 参数如果设为 True，把不同参数类型得到的结果分开保存，即把通常认为相等的浮点数和整数参数（如 1 和 1.0）区分开。，因为 lru_cache 使用字典存储结果，而且键根据调用时传
入的定位参数和关键字参数创建，所以被 lru_cache 装饰的函数，它
的所有参数都必须是可散列的。

单分派函数
from functools import singledispatch
from collections import abc
import numbers
import html

@singledispatch ➊
def htmlize(obj):
	content = html.escape(repr(obj))
	return '<pre>{}</pre>'.format(content)

@htmlize.register(str) ➋
def _(text): ➌
	content = html.escape(text).replace('\n', '<br>\n')
	return '<p>{0}</p>'.format(content)
	
@htmlize.register(numbers.Integral) ➍
def _(n):
	return '<pre>{0} (0x{0:x})</pre>'.format(n)
	
@htmlize.register(tuple) ➎
@htmlize.register(abc.MutableSequence)
def _(seq):
	inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
	return '<ul>\n<li>' + inner + '</li>\n</ul>'
	
❶ @singledispatch 标记处理 object 类型的基函数。
❷ 各个专门函数使用 @«base_function».register(«type») 装饰。
❸ 专门函数的名称无关紧要；_ 是个不错的选择，简单明了。
❹ 为每个需要特殊处理的类型注册一个函数。numbers.Integral 是
int 的虚拟超类。
❺ 可以叠放多个 register 装饰器，让同一个函数支持不同类型。
只要可能，注册的专门函数应该处理抽象基类（如 numbers.Integral
和 abc.MutableSequence），不要处理具体实现（如 int 和
list）。这样，代码支持的兼容类型更广泛。例如，Python 扩展可以子
类化 numbers.Integral，使用固定的位数实现 int 类型。

装饰器工厂
register = set() ➊
def register(active=True): ➋
	def decorate(func)
		print('running register(active=%s)->decorate(%s)'
% (active, func))
	if active: ➍
		registry.add(func)
	else:
		registry.discard(func)
	return func
	
return decorate

@register(active=False) ➑
def f1():
	print('running f1()')
	
@register() ➒
def f2():
	print('running f2()')
	
def f3():
	print('running f3()')

只有 active 参数的值（从闭包中获取）是 True 时才注册 func。
decorate 是装饰器，必须返回一个函数。
register 是装饰器工厂函数，因此返回 decorate。
@register 工厂函数必须作为函数调用，并且传入所需的参数。
即使不传入参数，register 也必须作为函数调用

带参数的装饰器
import time
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT)
	def decorate(func)
		def clocked(*_args)
			t0 = time.time()
			_result = func(*_args) ➍
			elapsed = time.time() - t0
			name = func.__name__
			args = ', '.join(repr(arg) for arg in _args) ➎
			result = repr(_result) ➏
			print(fmt.format(**locals())) ➐
			return _result ➑
		return clocked ➒
	return decorate ➓
	
if __name__ == '__main__':
	@clock()
	def snooze(seconds):
		time.sleep(seconds)
		
	for i in range(3):
		snooze(.123)
		
❶ clock 是参数化装饰器工厂函数。
❷ decorate 是真正的装饰器。
❸ clocked 包装被装饰的函数。
❹ _result 是被装饰的函数返回的真正结果。
❺ _args 是 clocked 的参数，args 是用于显示的字符串。
❻ result 是 _result 的字符串表示形式，用于显示。
❼ 这里使用 **locals() 是为了在 fmt 中引用 clocked 的局部变量。
❽ clocked 会取代被装饰的函数，因此它应该返回被装饰的函数返回
的值。
❾ decorate 返回 clocked。
❿ clock 返回 decorate。
⓫ 在这个模块中测试，不传入参数调用 clock()，因此应用的装饰器
使用默认的格式 str。

import time
from clockdeco_param import clock
@clock('{name}: {elapsed}s') #这个参数是输出格式
def snooze(seconds):
	time.sleep(seconds)
	
for i in range(3):
	snooze(.123)
输出：
$ python3 clockdeco_param_demo1.py
snooze: 0.12414693832397461s
snooze: 0.1241159439086914s
snooze: 0.12412118911743164s

