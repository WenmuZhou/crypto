## 一、简介
&emsp;&emsp;在回测或者交易的时候，我们要能够分析交易系统的效果。不仅仅要知道系统的收益，还需要知道系统的风险，以及是否比基准要好。因此就需要analyzer。    
## 二、Analyzer用法
&emsp;&emsp;Analyzer是加载到Cerebro实例中的：
```python
import backtrader as bt

cerebro = bt.Cerebro()
cerebro.addanalyzer(ancls, *args, **kwargs)
```
ancls在cerebro.run()中用输入的参数进行实例化，并且每个策略都会用到Analyzer。也就是说如果回测中有3个策略，则会把这个analyzer实例化3个，每个analyzer对应一个策略。Analyzer是针对策略的，而不是整个系统的。   
## 三、Backtrader提供的Analyzers
&emsp;&emsp;Backtrader提供了10多种Analyzers，每个Analyzer都有一个get_analysis()方法用于获取结果。
### 3.1 年化收益(AnnualReturn)
```python
class backtrader.analyzers.AnnualReturn()
```
这个Analyzer用年初和年末的数据计算年化收益。有以下两个属性：
- rets:年化收益的列表
- ret: 年化收益的字典

获取数据的方法：  
- get_analysis: 返回字典型的年化收益

### 3.2 卡玛比率(Calmar)
```python
class backtrader.analyzers.Calmar()
```
&emsp;&emsp;Calmar比率用于衡量收益风险比。用年化收益以最大回撤得到Calmar比率。可以设置以下参数：
- timeframe：默认为None。如果为None，采用第一个数据的时间表；如果设置为TimeFrame.NoTimeFrame，则没有时间限制
- compression：默认为None。仅用于分日时间表。比如时间表指定为TimeFrame.Minutes，则60条数据压缩
- fund：默认为None。如果为None，将自动检测经纪人的模式，以确定是基于全部净资产还是基金价值计算的收益。

获取数据的方法：  
- get_analysis：返回一个顺序字典，包含时间和Calmar比率

### 3.3 回撤(DrawDown)
```python
class backtrader.analyzers.DrawDown()
```
&emsp;&emsp;计算交易系统的回撤、最大回撤。可设置的单数为：
- fund：默认为None。如果为None，将自动检测经纪人的模式，以确定是基于全部净资产还是基金价值计算的收益。

获取数据方法：
- get_analysis：返回一个字典，包含如下键/值:
  - drawdown: 回撤值 （%）
  - moneydown: 资金回撤值
  - len: 回撤时间跨度
  - max.drawdown:   最大回撤(%)
  - max.moneydown:  最大资金回撤
  - max.len:        最大回撤时间跨度

### 3.4 时间回撤(TimeDrawDown)
```python
class backtrader.analyzers.TimeDrawDown()
```
&emsp;&emsp;用选定的时间表计算交易系统的回撤。可设置的参数为：
- timeframe: 默认为None。如果为None，采用第一个数据的时间表；如果设置为TimeFrame.NoTimeFrame，则没有时间限制
- compression：默认为None。仅用于分日时间表。比如时间表指定为TimeFrame.Minutes，则60条数据压缩
- fund：默认为None。如果为None，将自动检测经纪人的模式，以确定是基于全部净资产还是基金价值计算的收益。

获取数据的方法：
- get_analysis：返回一个字典数据：
  - drawdown：回撤值
  - maxdrawdown：资金最大回撤值
  - maxdrawdownperoid：回撤时间跨度

### 3.5 总杠杆(GrossLeverage)
```python
class backtrader.analyzers.GrossLeverage()
```
&emsp;&emsp;计算当前策略的总杠杆率。可设置的参数：
- fund：默认为None。如果为None，将自动检测经纪人的模式，以确定是基于全部净资产还是基金价值计算的收益。

获取数据的方法：
- get_analysis()：返回一个字典数据

### 3.6 组合投资(PyFolio)
```python
class backtrader.analyzers.PyFolio()
```

### 3.7 头寸价值(PositionsValue)
```python
class backtrader.analyzers.PositionsValue()
```
&emsp;&emsp;计算当前数据集头寸的价值。可设置的参数如下：
- timeframe: 默认为None。如果为None，采用第一个数据的时间表；如果设置为TimeFrame.NoTimeFrame，则没有时间限制
- compression：默认为None。仅用于分日时间表。比如时间表指定为TimeFrame.Minutes，则60条数据压缩
- headers：默认为False。增加一个键
- case：默认为False。是否把真实资金作为一个额外的头寸

获取数据的方法：
get_analysis：返回一个字典数据

### 3.8 (LogReturnsRolling)
```python
class backtrader.analyzers.LogReturnsRolling()
```
&emsp;&emsp;计算给定时间内的滚动收益。

### 3.9 统计数据(PeriodStats)
```python
class backtrader.analyzers.PeriodStats()
```
&emsp;&emsp;计算给定的时间内的统计数据。获取的数据如下：
- average
- stddev
- positive
- negative
- nochange
- best
- worst

### 3.10 收益(Returns)
```python
class backtrader.analyzers.Returns()
```

### 3.11 夏普率(SharpeRatio)
```python
class backtrader.analyzers.SharpeRatio()
```
&emsp;&emsp;计算策略的夏普率。

### 3.12 夏普率A(SharpeRatio_A)
```python
class backtrader.analyzers.SharpeRatio_A()
```
&emsp;&emsp;夏普率的扩展。计算年化夏普率

### 3.13 系统质量指数(SQN)
```python
class backtrader.analyzers.SQN()
```
&emsp;&emsp;计算系统的质量。

### 3.14 时间收益(TimeReturn)
```python
class backtrader.analyzers.TimeReturn()
```
&emsp;&emsp;根据给定时间首末数据计算收益。

### 3.15 交易分析(TradeAnalyzer)
```python
class backtrader.analyzers.TradeAnalyzer()
```
&emsp;&emsp;统计交易结束的数据。

### 3.16 交易(Transactions)
```python
class backtrader.analyzers.Transactions()
```
&emsp;&emsp;记录系统中每个数据的交易。

### 3.17 加权可变收益VWR(VWR)
```python
class backtrader.analyzers.VWR()
```
&emsp;&emsp;改进版的对数夏普率。可设置的参数有：
- timeframe: 默认为None。如果为None，在回测整个时间上计算；如果设置为TimeFrame.NoTimeFrame，则没有时间限制
- compression：默认为None。仅用于分日时间表。比如时间表指定为TimeFrame.Minutes，则60条数据压缩
- tann：默认None。计算平均收益的时间。如果为None，则用标准的值：
  - days: 252
  - weeks: 52
  - months: 12
  - years: 1
- tau：默认2.0。计算因子
- sdev_max：默认0.20。最大标准差
- fund：默认为None。如果为None，将自动检测经纪人的模式，以确定是基于全部净资产还是基金价值计算的收益





