## 一、简介
&emsp;&emsp;broker也就是经纪人/商，对应于证券交易所等。订单在这里进行处理。Backtrader里实现了几种不同的broker，主要是为了实盘时连接不同的交易所。我们针对回测时用的BackBroker()进行介绍。  
## 二、经纪人类
```python
class backtrader.brokers.BackBroker()
```
&emsp;&emsp;回测时，创建Cerebro()对象时，就创建了broker对象，并将其作为Cerebro对象的一个属性。Cerebro创建的broker()是默认的，我们也可以创建所需要的broker对象：
```python
cerebro = bt.Cerebro()
cerebro.broker = MyBroker()
```
&emsp;&emsp;broker有如下的参数：
- cash：初始资金，默认10000
- commission：佣金
- checksubmit：接收订单前，检查资金是否够，默认True
- filler：在一定时间里，多少成交量来匹配订单。默认为None
- slip_perc：按照价格的比例计算滑点，默认0.0
- slip_fixed：按照固定的数值计算滑点，默认0.0
- slip_open：计算滑点时候用下一个bar的开盘价，默认False
- slip_match：如果为True，将会避免滑点超过最高/最低价；如果设为False，broker将会在下一个bar执行。默认为True
- slip_limit：限价单是没有滑点的。如果为True，订单将会在最高价和最低价之间执行；如果为False，价格超过最低和最高价，将不会执行。默认为True
- slip_out：即使价格超出了最高价-最低价范围，也提供滑点。默认为False
- coc：cheat-on-close使能set_coc，也就是使用bar的收盘价成交，默认False
- coo：cheat-on-open使能set_coo，使用开盘价成交，默认False
- int2pnl：利息转换成pnl。默认True
- shortcash：如果为True，做空的时候资金增加，并且资产是负的；如果为False，做空时候资金减少，资产为正数。默认为True
- fundstartval：这个参数设置当用基金方式进行绩效评估时的起始值。默认100.0
- fundmode：如果设置为True，analyzers在进行评价时采用基金净值而不是总资产值。默认False

&emsp;&emsp;broker有如下的方法：
- set_cash(cash)：设置起始资金。setcash
- get_cash()：返回当前的资金。getcash
- get_value(datas=None, mkt=False, lever=False)：返回给定数据上的资产，如果datas=None，则返回总的组合资产。getvalue
- set_eosbar(eosbar)：设置eosbar参数。seteosbar
- set_checksubmit(checksubmit)：设置checksubmit参数
- set_filler(filler)：给filling模式设置成交量
- set_coc(coc)：配置cheat-on-close模式
- set_coo(coo)：配置cheat-on-open
- set_int2pnl(int2pnl)：将利息分给pnl
- set_fundstartval(fundstartval)：设置基金绩效模式的初始值
- set_slippage_perc(perc, slip_open=True, slip_limit=True, slip_match=True, slip_out=False)：设置百分比滑点
- set_slippage_fixed(fixed, slip_open=True, slip_limit=True, slip_match=True, slip_out=False)：设置固定值滑点
- get_orders_open(safe=False)：返回没有执行或者部分执行的订单
- getcommissioninfo(data)：获取一个数据的佣金信息
- setcommission(commission=0.0, margin=None, mult=1.0, commtype=None, percabs=True, stocklike=False, interest=0.0, interest_long=False, leverage=1.0, automargin=False, name=None)：设置佣金
- addcommissioninfo(comminfo, name=None)：增加佣金信息对象。如果name为none，则对所有资产增加
- getposition(data)：获取某个数据的仓位信息
- get_fundshares()：获取当前基金的份额
- get_fundvalue()：获取基金净值
- add_cash(cash)：增加或减少资金（负数减少资金）
