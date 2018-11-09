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










with 语句会设置一个临时的上下文，交给上下文管理器对象控制，并
且负责清理上下文。这么做能避免错误并减少样板代码，因此 API 更安
全，而且更易于使用。除了自动关闭文件之外，with 块还有很多用
途。


























































































































































