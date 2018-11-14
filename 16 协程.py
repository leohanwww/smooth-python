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

预激活协程的装饰器
from funtools import warps
def coroutine(func):
@warps(func)
def primer(*args, **kwargs)
	gen = func(*args, **kwargs)
	next(gen)
	return gen
return primer
把被装饰的生成器函数替换成这里的 primer 函数；调用 primer 函
数时，返回预激后的生成器。
from coroutil import coroutine ➍
@coroutine ➎
def averager():
...

终止协程和异常处理
协程中未处理的异常会向上冒泡，传给 next 函数或 send 方法的调用
方（即触发协程的对象）

generator.throw(exc_type[, exc_value[, traceback]])
　　致使生成器在暂停的 yield 表达式处抛出指定的异常。如果生成
器处理了抛出的异常，代码会向前执行到下一个 yield 表达式，而产
出的值会成为调用 generator.throw 方法得到的返回值。如果生成器
没有处理抛出的异常，异常会向上冒泡，传到调用方的上下文中。
generator.close()
　　致使生成器在暂停的 yield 表达式处抛出 GeneratorExit 异常。
如果生成器没有处理这个异常，或者抛出了 StopIteration 异常（通
常是指运行到结尾），调用方不会报错。如果收到 GeneratorExit 异
常，生成器一定不能产出值，否则解释器会抛出 RuntimeError 异常。
生成器抛出的其他异常会向上冒泡，传给调用方。
处理异常
class DemoException(Exception):
"""为这次演示定义的异常类型。"""
def demo_exc_handling():
	print('-> coroutine started')
	while True:
		try:
			x = yield
		except DemoException:
			print('*** DemoException handled. Continuing...')
		else:
			print('-> coroutine received: {!r}'.format(x))
	raise RuntimeError('This line should never run.') #这行代码不会执行，因为只有未处理的异常才会中止那个无限循环，而一旦出现未处理的异常，协程会立即终止。
激活和关闭协程，不发送异常
>>> exc_coro = demo_exc_handling()
>>> next(exc_coro)
-> coroutine started
>>> exc_coro.send(11)
-> coroutine received: 11
>>> exc_coro.send(22)
-> coroutine received: 22
>>> exc_coro.close()
>>> from inspect import getgeneratorstate
>>> getgeneratorstate(exc_coro)
'GEN_CLOSED'

传入DemoException
>>> exc_coro = demo_exc_handling()
>>> next(exc_coro)
-> coroutine started
>>> exc_coro.send(11)
-> coroutine received: 11
>>> exc_coro.throw(DemoException)
*** DemoException handled. Continuing...
>>> getgeneratorstate(exc_coro)
'GEN_SUSPENDED'
异常被处理了，协程的状态显示在等待状态

但是，如果传入协程的异常没有处理，协程会停止，即状态变成
'GEN_CLOSED'。
>>> exc_coro = demo_exc_handling()
>>> next(exc_coro)
-> coroutine started
>>> exc_coro.send(11)
-> coroutine received: 11
>>> exc_coro.throw(ZeroDivisionError)
Traceback (most recent call last):
...
ZeroDivisionError
>>> getgeneratorstate(exc_coro)
'GEN_CLOSED'

from collections import namedtuple
Result = namedtuple('Result', 'count average')
def averager():
	total = 0.0
	count = 0
	while True:
		term = yield
		if term =None:
			break #给的判断条件，让协程退出
		total += term
		count += 1
		average = total/count
	return Result(count, average)

>>> coro_avg = averager()
>>> next(coro_avg)
>>> coro_avg.send(10) ➊
>>> coro_avg.send(30)
>>> coro_avg.send(6.5)
>>> coro_avg.send(None) ➋
Traceback (most recent call last):
...
StopIteration: Result(count=3, average=15.5)

>>> coro_avg = averager()
>>> next(coro_avg)
>>> coro_avg.send(10)
>>> coro_avg.send(30)
>>> coro_avg.send(6.5)
>>> try:
... coro_avg.send(None)
... except StopIteration as exc:
... result = exc.value
...
>>> result
Result(count=3, average=15.5)

使用yield from不仅能捕获StopIter异常，还能把value属性的值变成yield from的值

def chain(*iterables)
	for it in iterables:
		yield form it
yield from x 表达式对 x 对象所做的第一件事是，调用 iter(x)，从
中获取迭代器。因此，x 可以是任何可迭代的对象。

yield from 的主要功能是打开双向通道，把最外层的调用方与最内层
的子生成器连接起来，这样二者可以直接发送和产出值，还可以直接传
入异常，而不用在位于中间的协程中添加大量处理异常的样板代码。有
了这个结构，协程可以通过以前不可能的方式委托职责。

委派生成器在 yield from 表达式处暂停时，调用方可以直
接把数据发给子生成器，子生成器再把产出的值发给调用方。子生
成器返回之后，解释器会抛出 StopIteration 异常，并把返回值附
加到异常对象上，此时委派生成器会恢复

from collections import namedtuple
Result = namedtuple('Result', 'count average')
#子生成器
def averager():
	total = 0.0
	count = 0
	average = None
	while True:
		term = yield
		if term is None: #等待
			break
		total += term
		count += 1
		average = total/count
		return Result(count, average)
#委派生成器
def grouper(result, key):
	while True:
		result[key] = yield from averager()
#在这里yield from起到传递值的作用，把group.send(value)传给子生成器的yield，而自己不知道传递的值是多少

#客户端代码，调用方
def main(data):
	result = {}
	for key, values in data.items():
		group = grouper()
		#外层 for 循环每次迭代会新建一个 grouper 实例，赋值给 group变量
		next(group) #预激委派生成器，进行到yield from处暂停
		for value in values:
			group.send(value) #把value发送给子生成器
		group.send(None)
#内层循环结束后，group 实例依旧在 yield from 表达式处暂停，因此，grouper 函数定义体中为 results[key] 赋值的语句还没有执行。
#如果外层 for 循环的末尾没有 group.send(None)，那么averager 子生成器永远不会终止，委派生成器 group 永远不会再次激活，因此永远不会为 results[key] 赋值。

report(results)

def report(results):
	for key, result in sorted(results.items)
		group, unit = key.split(';')
		print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))

data = {
	'girls;kg':
		[40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
	'girls;m':
		[1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
	'boys;kg':
		[39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
	'boys;m':
		[1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

if __name__ == '__main__':
	main(data)


传入委派生成器的异常，除了 GeneratorExit 之外都传给子生成
器的 throw() 方法。如果调用 throw() 方法时抛出
StopIteration 异常，委派生成器恢复运行。
如果把 GeneratorExit 异常传入委派生成器，或者在委派生成器
上调用 close() 方法，那么在子生成器上调用 close() 方法，如
果它有的话

出租车离散时间模拟
Event = collections.namedtuple('Event', 'time proc action')
#在 Event 实例中，time 字段是事件发生时的仿真时间，proc 字段是出租车进程实例的编号，action 字段是描述活动的字符串
def taxi_process(ident, trips, start_time=0):
	"""每次改变状态时创建事件，把控制权让给仿真器"""
#每辆出租车调用一次 taxi_process 函数，创建一个生成器对象，表示各辆出租车的运营过程。ident 是出租车的编号（如上述运行示例中的 0、1、2）；trips 是出租车回家之前的行程数量；start_time是出租车离开车库的时间。
	time = yield Event(start_time, ident, 'leave garage')
#产出的第一个 Event 是 'leave garage'。执行到这一行时，协程会暂停，让仿真主循环着手处理排定的下一个事件。需要重新激活这个进程时，主循环会发送（使用 send 方法）当前的仿真时间，赋值给time。
	for i in range(trips):
		yield Event(time, ident, 'pick up passenger')
#产出一个 Event 实例，表示拉到乘客了。协程在这里暂停。需要重新激活这个协程时，主循环会发送（使用 send 方法）当前的时间。
		yield Event(time, ident, 'drop off passenger')
#产出一个 Event 实例，表示乘客下车了。协程在这里暂停，等待主循环发送时间，然后重新激活
	yield Event(time, ident, 'going home')
#指定的行程数量完成后，for 循环结束，最后产出 'going home'事件。此时，协程最后一次暂停。仿真主循环发送时间后，协程重新激活；不过，这里没有把产出的值赋值给变量，因为用不到了。
#协程执行到最后时，生成器对象抛出 StopIteration 异常。

>>> from taxi_sim import taxi_process
>>> taxi = taxi_process(ident=13, trips=2, start_time=0) ➊
#trips=2表示两次上下客
>>> next(taxi) ➋
Event(time=0, proc=13, action='leave garage')
#此时在yield Event处暂停，等待下个事件
>>> taxi.send(_.time + 7) ➌
Event(time=7, proc=13, action='pick up passenger') ➍
>>> taxi.send(_.time + 23) ➎
Event(time=30, proc=13, action='drop off passenger')
>>> taxi.send(_.time + 5) ➏
Event(time=35, proc=13, action='pick up passenger')
>>> taxi.send(_.time + 48) ➐
Event(time=83, proc=13, action='drop off passenger')
>>> taxi.send(_.time + 1)
Event(time=84, proc=13, action='going home') ➑
>>> taxi.send(_.time + 10) ➒
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
StopIteration











































































































































































































