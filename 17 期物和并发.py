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
		res = executor.map(download_one, sorted(cc_list)) #返回一个迭代器
	return len(list(res))

if __name__ == '__main__':
	main(download_many)

标准库中有两个名为 Future 的
类：concurrent.futures.Future 和 asyncio.Future。这两个类的
作用相同：两个 Future 类的实例都表示可能已经完成或者尚未完成的
延迟计算
期物封装待完成的操作，可以放入队列，完成的状态可以查询，得到结
果（或抛出异常）后可以获取结果（或异常）。
from concurrent import futures
ThreadPoolExecutor我管这个叫线程池,如上面的例子，创建若干线程

使用execute.submit排定期物和as_completed期物列表检查期物
def download_many(cc_list):
	with futures.ThreadPoolExecutor(max_workers=3) as executor:
		to_do = []
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


































































































































































