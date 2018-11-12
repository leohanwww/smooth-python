第十五章

else语句

for/else模式
仅当 for 循环运行完毕时（即 for 循环没有被 break 语句中止）
才运行 else 块。
for item in my_list: #for运行完成表示item不在my_list里
	if item == 'banana':
		break
else:
	raise ValueError('No banana found') #不在循环里才执行

while/else模式
仅当 while 循环因为条件为假值而退出时（即 while 循环没有被
break 语句中止）才运行 else 块。

try模式
try:
	dangerous_call()
except OSError:
	log('OSError...')
else:
	after_call()
try 块防守的是 dangerous_call() 可能出现的错误，而
不是 after_call()。而且很明显，只有 try 块不抛出异常，才会执行
after_call()。
python的风格是EAFP，取得原谅比获得许可容易（easier to ask for forgiveness than
permission）。这是一种常见的 Python 编程风格，先假定存在有效
的键或属性，如果假定不成立，那么捕获异常。这种风格简单明
快，特点是代码中有很多 try 和 except 语句。与其他很多语言一
样（如 C 语言），这种风格的对立面是 LBYL 风格。

上下文管理器和with块
上下文管理器协议包含 __enter__ 和 __exit__ 两个方法。with 语句
开始运行时，会在上下文管理器对象上调用 __enter__ 方法。with 语
句运行结束后，会在上下文管理器对象上调用 __exit__ 方法，以此扮
演 finally 子句的角色。
>>> with open('mirror.py') as fp: # ➊__enter__方法返回self
... src = fp.read(60) # ➋
...
>>> len(src)
60
>>> fp # ➌
<_io.TextIOWrapper name='mirror.py' mode='r' encoding='UTF-8'>
>>> fp.closed, fp.encoding # ➍fp可用
(True, 'UTF-8')
>>> fp.read(60) # ➎但是fp不能操作，with结尾会默认调用__exit__方法
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file.

with 语句会设置一个临时的上下文，交给上下文管理器对象控制，并
且负责清理上下文。这么做能避免错误并减少样板代码，因此 API 更安
全，而且更易于使用。除了自动关闭文件之外，with 块还有很多用
途。

class LookingGlass:
	def __enter__(self): ➊#调用 __enter__ 方法时不传入其他参数
		import sys
		self.original_write = sys.stdout.write ➋
		sys.stdout.write = self.reverse_write ➌#替换标准输出为reverse
		return 'JABBERWOCKY' ➍#print(what)回调用标准输出
	def reverse_write(self, text): ➎
		self.original_write(text[::-1])
	def __exit__(self, exc_type, exc_value, traceback): ➏
		import sys ➐
		sys.stdout.write = self.original_write ➑#把标准输出改回原来的
		if exc_type is ZeroDivisionError: ➒
			print('Please DO NOT divide by zero!')
			return True ➓

>> from mirror import LookingGlass
>>> with LookingGlass() as what: ➊
... print('Alice, Kitty and Snowdrop') ➋
... print(what)
...
pordwonS dna yttiK ,ecilA ➌
YKCOWREBBAJ
>>> what ➍
'JABBERWOCKY'

>>> from mirror import LookingGlass
>>> manager = LookingGlass() ➊
>>> manager
<mirror.LookingGlass object at 0x2a578ac>
>>> monster = manager.__enter__() ➋
>>> monster == 'JABBERWOCKY' ➌
eurT
>>> monster
'YKCOWREBBAJ'
>>> manager
>ca875a2x0 ta tcejbo ssalGgnikooL.rorrim<
>>> manager.__exit__(None, None, None) ➍
>>> monster
'JABBERWOCKY'

contextlib模块中的实用工具
使用@contextmanager
@contextmanager 装饰器能减少创建上下文管理器的样板代码量，因
为不用编写一个完整的类，定义 __enter__ 和 __exit__ 方法，而只
需实现有一个 yield 语句的生成器，生成想让 __enter__ 方法返回的
值。


在使用 @contextmanager 装饰的生成器中，yield 语句的作用是把函
数的定义体分成两部分：yield 语句前面的所有代码在 with 块开始时
（即解释器调用 __enter__ 方法时）执行， yield 语句后面的代码在
with 块结束时（即调用 __exit__ 方法时）执行。

import contextlib
#contextlib.contextmanager 装饰器会把函数包装成实现__enter__ 和 __exit__ 方法的类。
@contextlib.contextmanager
def lookingglass():#yield之前属于with
	import sys
	original_write = sys.stdout.write #猴子补丁
	
	def reverse_write(text):
		original_write(text[::-1])
	
	sys.stdou.write = reverse_write
	yield 'JABBERWOCKY' ➎
	#产出一个值，这个值会绑定到 with 语句中 as 子句的目标变量上。
	sys.stdout.write = original_write ➏#调用__exit__方法

>>> from mirror_gen import looking_glass
>>> with looking_glass() as what: ➊
... print('Alice, Kitty and Snowdrop')
... print(what)
...
pordwonS dna yttiK ,ecilA
YKCOWREBBAJ
>>> what
'JABBERWOCKY'

使用 @contextmanager 装饰器时，要把 yield 语句放在
try/finally 语句中（或者放在 with 语句中），这是无法避免
的，因为我们永远不知道上下文管理器的用户会在 with 块中做什
么。
msg = ''
	try:
		yield 'JABBERWOCKY'
	except ZeroDivisionError:
		msg = ''DO NOT divide by zero
	finally:
		sys.stdout.write = original_write
		if msg:
			print(msg)

用于原地重写文件的上下文管理器
import csv
with inplace(csvfilename, 'r', newline='') as (infh, outfh):
#inplace 函数是个上下文管理器，为同一个文件提供了两个句柄（这个示例中的 infh 和 outfh），以便同时读写同一个文件。
	reader = csv.reader(infh)
	writer = csv.wirter(outfh)
	for row in reader:
		row += ['new', 'columns']
		writer.writerow(row)

























































































































