第十六章

yield item 这行代码会产出一
个值，提供给 next(...) 的调用方；此外，还会作出让步，暂停执行
生成器，让调用方继续工作，直到需要使用另一个值时再调用
next()。调用方会从生成器中拉取值。
在协程中，yield 通常出现在表达式的右边（例
如，datum = yield），可以产出值，也可以不产出——如果 yield
关键字后面没有表达式，那么生成器产出 None。协程可能会从调用方
接收数据，不过调用方把数据提供给协程使用的是 .send(datum) 方
法，而不是 next(...) 函数。通常，调用方会把值推送给协程。

yield item 产出值
data = yield 接收值

协程是指一个过程，这个过程与调用方协作，产出由调用方提供的值。

用作协程的生成器
def simple_coroutine():
	print('start')
	x = yield
	print('recived x:', x)
>>> my_coro = simple_coroutine()
>>>next(my_coro)
>>>start
>>>my_coro.send(42)
>>>recived x: 42
Traceback (most recent call last): # 
...
StopIteration

协程可以身处四个状态中的一个。当前状态可以使用
inspect.getgeneratorstate(...) 函数确定，该函数会返回下述字
符串中的一个。
'GEN_CREATED'
　　等待开始执行。
'GEN_RUNNING'
　　解释器正在执行。
'GEN_SUSPENDED'
　　在 yield 表达式处暂停。
'GEN_CLOSED'
　　执行结束。
因为 send 方法的参数会成为暂停的 yield 表达式的值，所以，仅当协
程处于暂停状态时才能调用 send 方法，例如 my_coro.send(42)。不
过，如果协程还没激活（即，状态是 'GEN_CREATED'），情况就不同
了。因此，始终要调用 next(my_coro) 激活协程——也可以调用
my_coro.send(None)，效果一样。
如果创建协程对象后立即把 None 之外的值发给它，会出现下述错误：
>>> my_coro = simple_coroutine()
>>> my_coro.send(1729)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: can't send non-None value to a just-started generator

>>> def simple_coro2(a):
... print('-> Started: a =', a)
... b = yield a
... print('-> Received: b =', b)
... c = yield a + b
... print('-> Received: c =', c)
...
>>> my_coro2 = simple_coro2(14)
>>> from inspect import getgeneratorstate
>>> getgeneratorstate(my_coro2) ➊
'GEN_CREATED'
>>> next(my_coro2) ➋
-> Started: a = 14
14 #这是yield a产出的值，并在这句后暂停
>>> getgeneratorstate(my_coro2) ➌
'GEN_SUSPENDED'
>>> my_coro2.send(28) ➍
-> Received: b = 28
42 #这是yield a + b产出的值，，= 右边的代码在赋值之前执行。因此，对于 b = yield a 这行代码来说，等到客户端代码再激活协程时才会设定 b 的值
>>> my_coro2.send(99) ➎
-> Received: c = 99
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
StopIteration
>>> getgeneratorstate(my_coro2) ➏
'GEN_CLOSED'

def avanger():
	total = 0.0
	count = 0
	while True:
		term = yield average
		total += term
		count += 1
		average = total/count
>>> coro_avg = averager() ➊
>>> next(coro_avg) ➋
>>> coro_avg.send(10) ➌
10.0
>>> coro_avg.send(30)
20.0
>>> coro_avg.send(5)
15.0
调用 next(coro_avg) 函数后，协程
会向前执行到 yield 表达式，产出 average 变量的初始值——None，
因此不会出现在控制台中。此时，协程在 yield 表达式处暂停，等到
调用方发送值。coro_avg.send(10) 那一行发送一个值，激活协程，把发送的值赋给 term，并更新 total、count 和 average 三个变量的
值，然后开始 while 循环的下一次迭代，产出 average 变量的值，等
待下一次为 term 变量赋值。因为averager没有初始值，所以next给average一个NONE的值































































































































































































































































































