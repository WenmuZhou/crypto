# crypto

crypto旨在打造一套丰富、领先、且实用的量化工具库，助力使用者开发出更好的策略，并早日实现财富自由。

## 1、安装

```
    git clone https://github.com/PKQ1688/crypto.git
    pip install -r requirements.txt
```

### 1.1 linux install ta_lib

### 1.1.1 安装ta-lib源码

```
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz #下载
    tar -xvf ta-lib-0.4.0-src.tar.gz  # 解压
    cd ta-lib # 进入目录
    ./configure --prefix=/usr
    make
    make install
```

### 1.1.2 安装python版本的ta_lib

```
    git clone https://github.com/mrjbq7/ta-lib.git
    cd ta-lib
    python setup.py install
```

### 1.1.3 解决bug

错误：`ImportError: libta_lib.so.0: cannot open shared object file: No such file or directory`

解决方案:

```
sudo find / -name libta_lib.so.0
/usr/lib/libta_lib.so.0
/root/ta-lib/src/.libs/libta_lib.so.0

vi /etc/profile
add
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib

source /etc/profile
```

## 2、回测部分
### 2.1 backtrader_base
&emsp;&emsp;本模块是基于backtrader进行开发的。我们对其进行了封装，以使开发者聚焦于策略的开发，而不用关心无关的事情。backtrader的官方文档：https://www.backtrader.com/docu/  
&emsp;&emsp;***封装说明：***  
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
    
&emsp;&emsp;***开发说明：***  
1）必须重写的方法  
&emsp;&emsp;必须重写cal_technical_index()和next()方法  
2）视情况决定是否重写  
&emsp;&emsp;data_process()在数据格式不满足要求时候重写  
&emsp;&emsp;***例子：***  
&emsp;&emsp;以双均线作为例子来说明如何在BasisStrategy()上开发策略。  
```python
import backtrader as bt
import pandas as pd

from strategy.backtrader_base.background_logic import BasisStrategy


class TwoSmaStrategy(BasisStrategy):
    params = (('short_period', 5), ('long_period', 10))  #策略参数，外部可更改
    def __init__(self):
        super(TwoSmaStrategy, self).__init__()

    @staticmethod
    def data_process(data_path):                        #重写数据处理方法
        df = pd.read_csv(data_path)
        df["date"] = pd.to_datetime(df["date"])
        data = bt.feeds.PandasData(dataname=df, datetime="date", volume="volume")
        return data

    def cal_technical_index(self):                      #重写指标计算方法
        print("short_period: ", self.params.short_period)
        print('long_period: ', self.params.long_period)
        self.sma5 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.short_period)  #短周期均线指标
        self.sma10 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.long_period)  #长周期均线指标

    def next(self):                                     #重写策略实现方法
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
    ret, cere = TwoSmaStrategy.run(
        data_path="dataset/hs300_d/sz.000001.csv",
        params_dict={"strategy_params": {"short_period": 5, "long_period": 10}, 
                     'analyzers':{'sharp': bt.analyzers.SharpeRatio, 'annual_return': bt.analyzers.AnnualReturn, 'drawdown': bt.analyzers.DrawDown}}
    )
    print('Sharpe Ratio: ', ret[0].analyzers.sharp.get_analysis())
    print('drawdown: ', ret[0].analyzers.drawdown.get_analysis())
    cere.plot(style='candle')
```
&emsp;&emsp;上面策略有两个参数：短周期和长周期，可通过传参修改，传入参数的键名和类参数中的字符串一致。  
&emsp;&emsp;回测指标的获取时，第三个属性和传参的键名一致。



## 3、线上交易部分(trading)

### 3.1 trade_execution

本部分代码主要用于策略的线上自动执行部分代码。<br>
根据不同的执行时间周期进行策略的划分。

### 3.2 trade_strategy

本部分代码主要用于策略算法的编写。<br>
策略执行的基本逻辑在`base_trading.py`中定义好了基本策略执行逻辑。<br>
定义新的策略只需要继承`BasisTrading`类，重写`strategy_trade`方法即可。<br>
示例代码：`two_ma.py`

```python
import talib
from trading.trade_strategy.base_trading import BasisTrading

class TwoMATrade(BasisTrading):
    # 构建自己的线上交易策略
    def strategy_trade(self, params):
        """

        :param params: 输入一些需要的参数
            coin_name: 操作的币种
            long_ma: 长期均线的时间周期
            short_ma: 短期均线的时间周期
            time_periods: 查看多少时间的
        :return:
            返回策略选定的需要买入的币种
        """
        coin_name = params.get("coin_name", "BTC")
        long_ma = params.get("long_ma", 10)
        short_ma = params.get("short_ma", 5)
        time_periods = params.get("time_periods", "4h")

        df = self.get_data(coin_name, time_periods, long_ma * 2)
        df["short_ma"] = talib.SMA(df["close"], timeperiod=short_ma)
        df["long_ma"] = talib.SMA(df["close"], timeperiod=long_ma)
        # print(df)
        print(df.tail(1))

        if df.tail(1)["short_ma"].item() > df.tail(1)["long_ma"].item():
            now_style = "REEF"
        else:
            now_style = "USDT"
        return now_style
```

## 4.数据获取

使用`get_data`里面的`get_kdata`可以获取历史数据<br>
参数选择

````
# 需要获取列表
coin_list = ["BTC", "ETH", "EOS", "FIL", "LTC", "XRP", "DOT", "KSM", "CAKE", "BNB", "ADA", "UNI"]
# 获取的K线的时间周期
time_period = "4h"
# 进行多少轮的数据获取
range_number = 10
# 每一轮获取到的数据(有些交易所的接口限制每次最多获取1000条数据）
limit_number = 1000
```
