第十八章

用线程实现的动态显示

import threading
import itertools
import time
import sys

class Signal:#定义只有单属性的类
	go = True
	
def spin(msg, signal):#单线程的函数，参数是signal类
	write, flush = sys.stdout.write, sys.stdout.flush
	for char in itertools.cycle('|/-\\'):
		status = char + ' ' + msg
		write(status)
		flush()
		write('\x08' * len(status))#输出退格符，定位到一行最前面
		time.sleep(.1)
		if not signal.go:#用signal从外部控制函数
			break
	write(' ' * len(status) + '\x08' * len(status))#使用空格清除状态消息，把光标移回开头。
	
def slow_function():
	time.sleep(3)#sleep会阻塞主线程
	return 42
	
def supervisor():#调用线程，显示对象，杀死线程
	signal = Signal
	spinner = threading.Thread(target=spin, args=('thinking!', signal))
	print('spinner object:', spinner)
	spinner.start()
	result = slow_function()#运行 slow_function 函数，阻塞主线程。
	signal.go = False#设置信号
	spinner.join()#等待线程自己退出
	return result
	
def main():
	result = supervisor()
	print('Answer:', result)

if __name__ == '__main__':
	main()
	

使用asyncio协程实现
import asyncio
import itertools
import sys

@asyncio.coroutine
def spin(msg):
	write, flush = sys.stdout.write, sys.stdout.flush
	for char in itertools.cycle('|/-\\')
		status = char + ' ' + msg
		write(status)
		flush()
		write('\x08' * len(status))
		try:
			yield from asyncio.sleep(.1)
#使用 yield from asyncio.sleep(.1) 代替 time.sleep(.1)，这样的休眠不会阻塞事件循环。
		except asyncio.CancelledError:
			break
	write(' ' * len(status) + '\x08' * len(status))
	
@asyncio.coroutine
def slow_function():
	yield from asyncio.sleep(3)
#把控制权交给主循环，在休眠结束后恢复这个协程。
	return 42

@asyncio.coroutine
def supervisor():
	spinner = asyncio.async(spin('thinking!'))
#asyncio.async(...) 函数排定 spin 协程的运行时间，使用一个Task 对象包装 spin 协程，并立即返回。
	print('spinner object:', spinner)
	result = yield from slow_function()
#驱动slow函数，获取返回值，同时循环继续进行，因为在slow中yield from把控制权交还给了主循环
	spinner.cancel()
	return result
	
def main():
	loop = asyncio.get_event_loop()#获取时间循环的引用
	result = loop.run_until_complete(supervisor())
#驱动 supervisor 协程，让它运行完毕；这个协程的返回值是这次调用的返回值。
	loop.close()
	print('Answer', result)
	
if __name__ == '__main__':
	main()
	
除非想阻塞主线程，从而冻结事件循环或整个应用，否则不
要在 asyncio 协程中使用 time.sleep(...)。如果协程需要在一
段时间内什么也不做，应该使用 yield from
asyncio.sleep(DELAY)。
使用 @asyncio.coroutine 装饰器不是强制要求，但是强烈建议这么
做，因为这样能在一众普通的函数中把协程凸显出来，也有助于调试：
如果还没从中产出值，协程就被垃圾回收了（意味着有操作未完成，因
此有可能是个缺陷），那就可以发出警告。这个装饰器不会预激协程。