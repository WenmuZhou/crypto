&emsp;&emsp;本文档是对基于backtrader开发的说明，目录为strategy/backtrader_base。
## 一、概况
&emsp;&emsp;为了简化基于backtrader开源库进行策略的开发，我们对backtrader进行了封装，使开发者聚焦于策略的实现，而不用关心无关的功能。  
&emsp;&emsp;backtrader的官方文档：https://www.backtrader.com/docu/
## 二、详细介绍
### 1、封装说明
&emsp;&emsp;background_logic.py模块中的类BasisStrategy()实现了对bt.strategy的封装，包含诸如日志打印等方法：
- log(txt, dt=None, doprint=False)：日志打印
    - txt: 打印的内容
    - dt: 时间，默认从数据获取时间
    - doprint: 打印开关，默认不打印
- __init__()：初始化
    - data_close：收盘价
    - order：订单
    - buy_price：买入价格
    - buy_comm：佣金
- cal_technical_index()：计算指标
    - 需要开发者自己实现。用于计算策略中用到的指标。比如双均线策略，需要在此方法中实现均线指标。
- next()：策略实现
    - 这个方法里实现策略。需要开发者自己实现。
- notify_order(order)：输出订单的状态
    - 这个方法输出订单的状态，开发者可以不用重写这个方法
- notify_trade(trade)：输出交易的收益
    - 这个方法输出交易的收益，开发者可以不用重写这个方法
- stop()：回测结束，输出账户最终资产
    - 这个方法输出最终资产，开发者可以不用重写这个方法
- data_process(data_path)：数据处理
    - 这个方法用于处理数据，使得数据符合backtrader的要求。开发者根据需要进行重写
- run(cls, data_path="", cash=100000, commission=1.5/1000, slip_type=-1, slip_value=0, params_dict={})：运行策略，返回
    - 这个方法运行策略，返回策略结果。一般可以不用重写。
    - data_path：数据路径
    - cash：初始资金
    - commission：佣金
    - slip_type：滑点类型。0：固定值滑点，1：百分比滑点，其他：没有滑点
    - slip_value：滑点值
    - params_dict：设置策略参数、回测指标
        - 策略参数的键名：strategy_params，对应的值的类型是字典，比如双均线的参数：{"strategy_params": {"short_period": 5, "long_period": 10}}
        - 回测指标的键名：analyzers，对应的值的类型是字典，比如夏普值和回撤：{'analyzers':{'sharp': bt.analyzers.SharpeRatio, 'drawdown': bt.analyzers.DrawDown}}
### 2、开发说明
#### 1）必须重写的方法
&emsp;&emsp;必须重写cal_technical_index()和next()方法
#### 2）视情况决定是否重写
&emsp;&emsp;data_process()在数据格式不满足要求时候重写
## 三、例子
&emsp;&emsp;以双均线作为例子来说明如何在BasisStrategy()上开发策略。

```python
import backtrader as bt
import pandas as pd

from strategy.backtrader_base.background_logic import BasisStrategy


class TwoSmaStrategy(BasisStrategy):
    params = (('short_period', 5), ('long_period', 10))  # 策略参数，外部可更改

    def __init__(self):
        super(TwoSmaStrategy, self).__init__()

    @staticmethod
    def data_process(data_path):  # 重写数据处理方法
        df = pd.read_csv(data_path)
        df["date"] = pd.to_datetime(df["date"])
        data = bt.feeds.PandasData(dataname=df, datetime="date", volume="volume")
        return data

    def cal_technical_index(self):  # 重写指标计算方法
        print("short_period: ", self.params.short_period)
        print('long_period: ', self.params.long_period)
        self.sma5 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.short_period)  # 短周期均线指标
        self.sma10 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.long_period)  # 长周期均线指标

    def next(self):  # 重写策略实现方法
        self.log('Close, %.2f' % self.data_close[0])

        if self.order:
            return

        if not self.position:
            if self.sma5[0] > self.sma10[0]:
                self.order = self.buy()
        else:
            if self.sma5[0] < self.sma10[0]:
                self.order = self.sell()


if __name__ == '__main__':
    ret, cere = TwoSmaStrategy.run(data_path="dataset/hs300_d/sz.000001.csv",
                                   params_dict={"strategy_params": {"short_period": 5, "long_period": 10},
                                                'analyzers': {'sharp': bt.analyzers.SharpeRatio,
                                                              'annual_return': bt.analyzers.AnnualReturn,
                                                              'drawdown': bt.analyzers.DrawDown}})
    print('Sharpe Ratio: ', ret[0].analyzers.sharp.get_analysis())
    print('drawdown: ', ret[0].analyzers.drawdown.get_analysis())
    cere.plot(style='candle')
```
&emsp;&emsp;上面策略有两个参数：短周期和长周期，可通过传参修改，传入参数的键名和类参数中的字符串一致。  
&emsp;&emsp;回测指标的获取时，第三个属性和传参的键名一致。


