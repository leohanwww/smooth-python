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

