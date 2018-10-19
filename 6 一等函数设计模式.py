第六章

使用函数实现“策略”模式
用函数取代类，作为参数传入实例，用作策略的模式

from collections import namedtuple
Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
        
    def total(self):
        return self.price * self.quantity
        
class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
        
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
        
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self) ➊
        return self.total() - discount
        
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())
        
def fidelity_promo(order): ➌
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0
        
def bulk_item_promo(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount
        
def large_order_promo(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0
    
>>> joe = Customer('John Doe', 0) ➊
>>> ann = Customer('Ann Smith', 1100)
>>> cart = [LineItem('banana', 4, .5),
... LineItem('apple', 10, 1.5),
... LineItem('watermellon', 5, 5.0)]
>>> Order(joe, cart, fidelity_promo) ➋
<Order total: 42.00 due: 42.00>
>>> Order(ann, cart, fidelity_promo)
<Order total: 42.00 due: 39.90>
>>> banana_cart = [LineItem('banana', 30, .5),
... LineItem('apple', 10, 1.5)]
>>> Order(joe, banana_cart, bulk_item_promo) ➌
<Order total: 30.00 due: 28.50>
>>> long_order = [LineItem(str(item_code), 1, 1.0)
... for item_code in range(10)]
>>> Order(joe, long_order, large_order_promo)
<Order total: 10.00 due: 9.30>
>>> Order(joe, cart, large_order_promo)
<Order total: 42.00 due: 42.00>

可以构建一个优惠策略选择
promos = [fidelity_promo, bulk_item_promo, large_order_promo] ➊
def best_promo(order): ➋
	"""选择可用的最佳折扣
	"""
	return max(promo(order) for promo in promos) ➌
	
通过找出模块里的全部策略
globals()
　　返回一个字典，表示当前的全局符号表。这个符号表始终针对当前
模块（对函数或方法来说，是指定义它们的模块，而不是调用它们的模
块）。
promos = [globals()[name] for name in globals() ➊
if name.endswith('_promo') ➋
and name != 'best_promo'] ➌
#这是一个列表生成式，生成模块方法里名字以_promo结尾的列表
def best_promo(order): ➋
	"""选择可用的最佳折扣
	"""
	return max(promo(order) for promo in promos) ➌
	
内省单独的 promotions 模块，构建 promos 列表
promos = [func for name, func in
                   inspect.getmembers(promotions, inspect.isfunction)]
#这个生成式获取模块promotions里的函数，
#inspect.getmembers 函数用于获取对象（这里是 promotions 模块）
#的属性，第二个参数是可选的判断条件（一个布尔值函数）。我们使用
#的是 inspect.isfunction，只获取模块中的函数。
def best_promo(order):
	"""选择可用的最佳折扣
	"""
	return max(promo(order) for promo in promos)