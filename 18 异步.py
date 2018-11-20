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
段时间内什么也不做，应该使用 yield from asyncio.sleep(DELAY)。
使用 @asyncio.coroutine 装饰器不是强制要求，但是强烈建议这么
做，因为这样能在一众普通的函数中把协程凸显出来，也有助于调试：
如果还没从中产出值，协程就被垃圾回收了（意味着有操作未完成，因
此有可能是个缺陷），那就可以发出警告。这个装饰器不会预激协程。

asyncio.async(coro_or_future, *, loop=None)
　　这个函数统一了协程和期物：第一个参数可以是二者中的任何一
个。如果是 Future 或 Task 对象，那就原封不动地返回。如果是协
程，那么 async 函数会调用 loop.create_task(...) 方法创建 Task
对象。loop= 关键字参数是可选的，用于传入事件循环；如果没有传
入，那么 async 函数会通过调用 asyncio.get_event_loop() 函数获
取循环对象。
BaseEventLoop.create_task(coro)
　　这个方法排定协程的执行时间，返回一个 asyncio.Task 对象。如
果在自定义的 BaseEventLoop 子类上调用，返回的对象可能是外部库
（如 Tornado）中与 Task 类兼容的某个类的实例。


使用asyncio和aiohttp包下载
import asyncio
import aiohttp 
from flags import BASE_URL, save_flag, show, main 

@asyncio.coroutine 
def get_flag(cc):
	url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
	resp = yield from aiohttp.request('GET', url) 
	image = yield from resp.read() 
	return image
	
@asyncio.coroutine
def download_one(cc):
	image = yield from get_flag(cc)
	show(cc)
	save_flag(image, cc.lower() + '.gif')
	return cc
	
def download_many(cc_list):
	loop = asyncio.get_event_loop()#获取事件循环底层实现的引用
	to_do = [download_one(cc) for cc in cc_list]
#创建待下载生成器对象列表
	wait_coro = asyncio.wait(to_do)
#asyncio.wait 是一个协程，等传给它的所有协程运行完毕后结束，返回一个生成器或协程
	res, _ = loop.run_until_complete(wait_coro)
#执行事件循环，直到 wait_coro 运行结束；事件循环运行的过程中，这个脚本会在这里阻塞
	loop.close()
	return len(res)
	
if __name__ == '__main__':
	main(download_many)
asyncio.wait(...) 协程的参数是一个由期物或协程构成的可迭代对
象；wait 会分别把各个协程包装进一个 Task 对象。最终的结果
是，wait 处理的所有对象都通过某种方式变成 Future 类的实
例。wait 是协程函数，因此返回的是一个协程或生成器对
象
loop.run_until_complete 方法的参数是一个期物或协程。如果是协
程，run_until_complete 方法与 wait 函数一样，把协程包装进一个
Task 对象中。协程、期物和任务都能由 yield from 驱动，这正是
run_until_complete 方法对 wait 函数返回的 wait_coro 对象所做
的事。wait_coro 运行结束后返回一个元组，第一个元素是一系列结束
的期物，第二个元素是一系列未结束的期物。在示例 18-5 中，第二个
元素始终为空，因此我们把它赋值给 _，将其忽略。

在 download_many 函数中调用
loop.run_until_complete 方法时，事件循环驱动各个
download_one 协程，运行到第一个 yield from 表达式处，那个表达
式又驱动各个 get_flag 协程，运行到第一个 yield from 表达式处，
调用 aiohttp.request(...) 函数。这些调用都不会阻塞，因此在零
点几秒内所有请求全部开始。
asyncio 的基础设施获得第一个响应后，事件循环把响应发给等待结果
的 get_flag 协程。得到响应后，get_flag 向前执行到下一个 yield
from 表达式处，调用 resp.read() 方法，然后把控制权还给主循环。
其他响应会陆续返回（因为请求几乎同时发出）。所有 get_ flag 协
程都获得结果后，委派生成器 download_one 恢复，保存图像文件。

使用asyncio.as_completed函数

import asyncio
import collections
import aiohttp
from aiohttp import web
import tqdm
from flags2_common import main, HTTPStatus, Result, save_flag

# 默认设为较小的值，防止远程网站出错
# 例如503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception): 
	def __init__(self, country_code):
		self.country_code = country_code
#这个自定义的异常用于包装其他 HTTP 或网络异常，并获取country_code，以便报告错误。
	
@asyncio.coroutine
def get_flag(base_url, cc):
	url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
	resp = yield from asyncio.request('GET', url)
	if resp.status == 200:
		image = yield from resp.read()
		return image
	elif resp.status == 404:
		raise web.HTTPNotFound()
	else:
		raise aiohttp.HttpProcessError(code=resp.status, message=resp.reason, headers=resp.headers)
			
@asyncio.coroutine
def download_one(cc, base_url, semaphore, verbose):
	try:#Semaphore 类是同步装置，用于限制并发请求数量。
		with(yield from semaphore):
#中把 semaphore 当成上下文管理器使用，防止阻塞整个系统：如果 semaphore 计数器的值是所允许的最大值，只有这个协程会阻塞。
#这段代码保证，任何时候都不会有超过 concur_req 个 get_flag 协程启动。
			image = yield from get_flag(base_url, cc)
	except web.HTTPNotFound:
		status = HTTPNotFound
		msg = 'not found'
	except Exception as exc:
		raise FetchError(cc) from exc
		#其他异常当作 FetchError 抛出，传入国家代码
	else:
		save_flag(image, cc.lower() + '.gif')
		status = HTTPStatus.ok
		msg = 'ok'
	if verbose and msg:
		print(cc, msg)
	return Result(status, cc)

@asyncio.coroutine
def downloader_coro(cc_list, base_url, verbose, concur_req):
	counter = collections.Counter()
	semaphore = asyncio.Semaphore(concur_req)
	#创建一个 asyncio.Semaphore 实例，最多允许激活 concur_req 个协程
	to_do = [download_one(cc, base_url, semaphore, verbose)
			for cc in sorted(cc_list)]
	to_do_iter = asyncio.completed(to_do)
	#期物容器
	if not verbose:
		to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
		#把迭代器传给 tqdm 函数，显示进度
	for future in to_do_iter:
		try:
			res = yield from future#获取 asyncio.Future 对象的结果
		except FetchError as exc:
			country_code = exc.country_code
			try:
				error_msg = exc.__cause__.args[0]
			except IndexError:
				error_msg = exc.__cause__.__class__.__name__
			if verbose and error_msg:
				msg = '*** Error for {}: {}'
				print(msg.format(country_code, error_msg))
			status = HTTPStatus.error_msg
		else:
			status = res.status
		
		counter[status] += 1
	return counter
	
def download_many(cc_list, base_url, verbose, concur_req):
	loop = asyncio.get_event_loop()
	coro = downloader_coro(cc_list, base_url, verbose, concur_req)
	counts = loop.run_until_complete(coro)
	loop.close()
	return counts
#download_many 函数只是实例化 downloader_coro 协程，然后通过 run_until_complete 方法把它传给事件循环。

if __name__ == '__main__':
	main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
	

还有服务器示例未完。。。
