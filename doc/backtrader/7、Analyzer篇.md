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



