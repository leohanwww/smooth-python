第十七章

期物指一种对象，表示异步
执行的操作。这个概念的作用很大，是 concurrent.futures 模块和
asyncio 包（第 18 章讨论）的基础。

使用concurrent.futures并发下载

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
'MX PH VN ET EG DE IR TR CD FR').split() 

BASE_URL = 'http://flupy.org/data/flags'

DEST_DIR = 'downloads/'

def save_flag(img, filename):
	path = os.path.join(DEST_DIR, filename)
	with open(path,'wb') as fp:
		fp.wirte(img)

def get_flag(cc):
	url = '{}/{cc}/{cc}'.format(BASE_URL, cc=cc.lower())
	resp = request.get(url)
	return resp.content

def show(text):
	print(text, end=' ')
	sys.stdout.flush()

def download_one(cc):
	image = get_flag(cc)
	show(cc)
	save_flag(imgage, cc.lower() + '.gif')
	return cc

def main(download_many):
	t0 = time.time()
	count = download_many(POP20_CC)
	elapsed = time.time() - t0
	msg = '\n{} flags downloaded in {:.2f}s'
	print(msg.format(count, elapsed))
	
MAX_WORKERS = 20

def download_many(cc_list):
	workers = min(MAX_WORKERS, len(cc_list))
#设定工作的线程数量：使用允许的最大值（MAX_WORKERS）与要处理的数量之间较小的那个值，以免创建多余的线程。
	with futures.ThreadPoolExecutor(workers) as executor:
#使用工作的线程数实例化 ThreadPoolExecutor类
		res = executor.map(download_one, sorted(cc_list)) #使用map方法，返回一个迭代器
	return len(list(res))

if __name__ == '__main__':
	main(download_many)

标准库中有两个名为 Future 的
类：concurrent.futures.Future 和 asyncio.Future。这两个类的
作用相同：两个 Future 类的实例都表示可能已经完成或者尚未完成的延迟计算
期物封装待完成的操作，可以放入队列，完成的状态可以查询，得到结
果（或抛出异常）后可以获取结果（或异常）。
from concurrent import futures
ThreadPoolExecutor我管这个叫线程池,如上面的例子，创建若干线程

使用execute.submit排定期物和as_completed期物列表检查期物
def download_many(cc_list):
	with futures.ThreadPoolExecutor(max_workers=3) as executor:
		to_do = [] #期物列表
		for cc in sorted(cc_list):
			future = executor.submit(download_one, cc)
#executor.submit 方法排定可调用对象的执行时间，然后返回一个期物，表示这个待执行的操作。
			to_do.append(future)
			msg = 'Scheduled for {}: {}'
			print(msg.format(cc, future))

		results = []
		for future in futures.as_completed(to_do): #as_completed 函数在期物运行结束后产出期物。
			res = future.result()
			msg = '{} result: {!r}'
			print(msg.format(future, res))
			results.append(res)

	return len(results)

使用 concurrent.futures 模块绕开线程锁GIL
def download_many(cc_list):
	workers = min(MAX_WORKERS, len(cc_list))
	with futures.ThreadPoolExecutor(workers) as executor:
改成
def download_many(cc_list):
	with future.ProcessPlloExecutor() as executor:
#进程池会自动获得cpu核心数并分派工作，不用手动指定进程数量


Executor.map使用方法
def main():
	display('Script starting.')
	executor = futures.ThreadPoolExecutor(max_workers=3) ➍#实例化
	results = executor.map(loiter, range(5)) ➎
	#立即显示调用 executor.map 方法的结果：一个生成器，
	display('results:', results) ➏
	display('Waiting for individual results:')
	for i, result in enumerate(results): ➐
		display('result {}: {}'.format(i, result))


显示下载进度并处理错误
def get_flag(base_url, cc):
	url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
	resp = requests.get(url)
	if resp.status_code != 200: ➊
		resp.raise_for_status()
	return resp.content

def download_one(cc, base_url, verbose=False):
	try:
		image = get_flag(base_url, cc)
	except requests.exceptions.HTTPError as exc:
		res = exc.response
		if res.status_code == 404:
			status = HTTPStatus.not_found
			msg = 'not found'
		else:
			raise
	else:
		save_flag(image, cc.lower() + '.gif')
		status = HTTPStatus.ok
		msg = 'OK'

	if verbose:
		print(cc, msg)
		
	return Results(status, cc)

def download_many(cc_list, base_url, verbose, max_req):
	counter = collections.counter()
	#这个 Counter 实例用于统计不同的下载状态：HTTPStatus.ok、HTTPStatus.not_found 或HTTPStatus.error。
	cc_iter = iter(cc_list)
	if not verbose:
		cc_iter = tqdm.tqdm(cc_iter)
		#如果不是详细模式，把 cc_iter 传给 tqdm 函数，返回一个迭代器，产出 cc_iter 中的元素，还会显示进度条动画。
	for cc in cc_iter:
		try:
			res = download_one(cc, base_url, verbose)
		except requests.exceptions.HTTPError as exc:
			error_msg = 'HTTP error {res.status_code} - {res.reason}'
			error_msg = error_msg.format(res=exc.response)
		except requests.exceptions.ConnectionError as exc:
			error_msg = 'Connection error'
		else:
			error_msg = ''
			status = res.status

		if error_msg:
			status = HTTPStatus.error
		counter[status] += 1
		if verbose and error_msg:
			print('*** Error for {}: {}'.format(cc, error_msg))

	return counter
#返回 counter，以便 main 函数能在最终的报告中显示数量。

使用futures.ThreadPoolExecutor类futures.as_completed函数
import collections
from concurrent import futures
import requests
import tqdm 
from flags2_common import main, HTTPStatus 
from flags2_sequential import download_one 

DEFAULT_CONCUR_REQ = 30 #默认线程池的大小，如果不指定的话
MAX_CONCUR_REQ = 1000 #最大的线程数量

def download_many(cc_list, base_url, verbose, concun_req):
	conter = collections.counter()
	with futures.ThreadPoolExecutor(max_workers=concun_req) as executor:
#把 max_workers 设为 concur_req，创建 ThreadPoolExecutor 实例
		to_do_map = {} #这个字典把各个 Future 实例（表示一次下载）映射到相应的国家代码上，在处理错误时使用
		for cc in sorted(cc_list):
			future = executor.submit(download_one, cc, base_url, verbose)
#每次调用 executor.submit 方法排定一个可调用对象的执行时间，然后返回一个 Future 实例
		to_do_map[future] = cc #把返回的 future 和国家代码存储在字典中。
	dont_iter = futures.as_completed(to_do_map)
#futures.as_completed 函数返回一个迭代器，在期物运行结束后产出期物
	if not verbose:
		dont_iter = tqdm.tqdm(dont_iter, total=len(cc_list))
#如果不是详细模式，把 as_completed 函数返回的结果传给 tqdm 函数，显示进度条
	for future in dont_iter: #迭代运行结束后的期物
		try:
			res = future.result()
#在期物上调用 result 方法，要么返回可调用对象的返回值，要么抛出可调用的对象在执行过程中捕获的异常。这个方法可能会阻塞，等待确定结果
		except requests.exceptions.HTTPError as exc: 
			error_msg = 'HTTP {res.status_code} - {res.reason}'
			error_msg = error_msg.format(res=exc.response)
		except requests.exceptions.ConnectionError as exc:
			error_msg = 'Connection error'
		else:
			error_msg = ''
			status = res.status
		if error_msg:
			status = HTTPStatus.error
			counter[status] += 1
		if verbose and error_msg:
			cc = to_do_map[future]
#为了给错误消息提供上下文，以当前的 future 为键，从to_do_map 中获取国家代码。
			print('*** Error for {}: {}'.format(cc, error_msg))
	return counter

if __name__ == '__main__'
	main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

用到了一个对 futures.as_completed 函数特别有用的惯
用法：构建一个字典，把各个期物映射到其他数据（期物运行结束后可
能有用）上。这里，在 to_do_map 中，我们把各个期物映射到对应的
国家代码上。这样，尽管期物生成的结果顺序已经乱了，依然便于使用
结果做后续处理。

