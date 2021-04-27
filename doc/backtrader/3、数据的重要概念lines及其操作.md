&emsp;&emsp;在流程的例子中，我们看计算均值指标的两行代码：
```python
self.sma_s = bt.indicators.MovingAverageSimple(self.datas[0].lines.close, period=self.params.short)#短期均线指标
self.sma_l = bt.indicators.MovingAverageSimple(self.datas[0].lines.close, period=self.params.long)#长期均线指标
```
计算数据用的是self.datas[0].lines.close。datas[0]表示取数据列表中的第一个数据，这个数据有个属性lines，lines里有属性close，计算均值指标用的是属性close的值。close表示的是收盘价，lines表示的是什么？lines翻译成中文表示多条线，为什么用线这个概念，直接用self.datas[0].close效果也是一样的，而且更直观。我猜想是为了和看盘术语一致，看盘我们看k线图，lines就类似于k线。默认的lines包含open, high, low, close, volume, openinterest这六条线。每条线都是由一系列点组成，通俗的说，就是数据数组。比如close这条线是由一段时间内收盘价组成的线。计算得到的均值sma_l和sma_s也是line。为了简单，datas[0]可以写成data，datas[x]可以写成datax。lines可以写成l。self.datas[0].lines.close可写成self.data.l.close或者self.data.close。   
&emsp;&emsp;策略里，对数据访问一般都是在next()方法里。通常访问下标为0的数据，也就是当前数据，-1表示上一个数据，-2是上两个数据，以此类推；1表示下一个数据，用1或其他正数，在数据到达末尾时会发生问题，因为数据访问越界了。每次进入next()，当前数据都自动向后移动一个。把流程里的代码简化下：
```python
import backtrader as bt
import pandas as pd

class TwoSmaStrategy(bt.Strategy):
    params = (('short', 5), ('long', 10))

    def __init__(self):
        # self.sma_s = bt.indicators.MovingAverageSimple(self.datas[0].lines.close, period=self.params.short)  # 短期均线指标
        self.sma_l = bt.indicators.MovingAverageSimple(self.datas[0].lines.close, period=self.params.long)  # 长期均线指标

    def next(self):
        dt = self.datas[0].datetime.date(0)
        print("date: {}, close_0: {}, close_-1: {}".format(dt.isoformat(), self.data.close[0], self.data.close[-1]))


if __name__ == '__main__':
    cerebro = bt.Cerebro()  
    
    data_path = './dataset/hs300_d/sz.000001.csv'
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    data = bt.feeds.PandasData(dataname=df, datetime='date')

    cerebro.addstrategy(TwoSmaStrategy, short=10, long=20)
    cerebro.adddata(data)
    ret = cerebro.run()  
```
输出的内容如下：  
date: 1991-05-06, close_0: 0.4246616, close_-1: 0.42902728  
date: 1991-05-07, close_0: 0.42257798, close_-1: 0.4246616  
date: 1991-05-08, close_0: 0.42049436, close_-1: 0.42257798  
date: 1991-05-09, close_0: 0.41841074, close_-1: 0.42049436  
date: 1991-05-10, close_0: 0.41632712, close_-1: 0.41841074  
date: 1991-05-13, close_0: 0.41215988, close_-1: 0.41632712  
date: 1991-05-14, close_0: 0.41007626, close_-1: 0.41215988  
date: 1991-05-15, close_0: 0.40799264, close_-1: 0.41007626  
date: 1991-05-16, close_0: 0.40590902, close_-1: 0.40799264  
下标-1的值和上一个下标0的值相同。打印输出的值从1991-5-6号开始的，而数据是从1991-4-3开始的。这是因为计算均值的周期是20，只能从第20个数据开始策略逻辑。如果计算周期是10，就从第10个数据开始，下面内容就是计算周期为10的内容：  
date: 1991-04-18, close_0: 0.45791424, close_-1: 0.4602078  
date: 1991-04-19, close_0: 0.45562068, close_-1: 0.45791424  
date: 1991-04-23, close_0: 0.44649, close_-1: 0.45562068  
date: 1991-04-24, close_0: 0.44430716, close_-1: 0.44649  
date: 1991-04-25, close_0: 0.44212432, close_-1: 0.44430716  
date: 1991-04-26, close_0: 0.43994148, close_-1: 0.44212432  
date: 1991-04-29, close_0: 0.4355758, close_-1: 0.43994148  
date: 1991-04-30, close_0: 0.43339296, close_-1: 0.4355758  
date: 1991-05-02, close_0: 0.43121012, close_-1: 0.43339296  
&emsp;&emsp;线的长度，也就是元素个数也很有意思。按照python习惯，用len()函数获取元素个数，计算指标的周期为10，next()里的print修改如下，其他不变：  
```python
print("date: {}, close_len: {}, sma_s_len: {}".format(dt.isoformat(), len(self.data.close), len(self.sma_s)))
```
得到的输出如下：   
date: 1991-04-18, close_len: 10, sma_s_len: 10  
date: 1991-04-19, close_len: 11, sma_s_len: 11  
date: 1991-04-23, close_len: 12, sma_s_len: 12  
date: 1991-04-24, close_len: 13, sma_s_len: 13  
date: 1991-04-25, close_len: 14, sma_s_len: 14  
......  
date: 2021-04-13, close_len: 7121, sma_s_len: 7121  
date: 2021-04-14, close_len: 7122, sma_s_len: 7122  
date: 2021-04-15, close_len: 7123, sma_s_len: 7123  
date: 2021-04-16, close_len: 7124, sma_s_len: 7124  
可以看出，不管是原始数据还是指标的长度都是从10开始，逐渐递增到最终长度7124。10是计算一个指标要用到的数据个数，也就是说len()表示的是用到的数据个数，每用一次，也就是执行一次next()，len就会加1；而且指标和原始数据的下标会自动对齐：第一次进入next，指标一次都没用过，但是长度为10，这是为了对齐，方便策略的实现。我们试试计算指标的长度设为1，看看打印输出长度从多少开始：  
date: 1991-04-03, close_len: 1, sma_s_len: 1  
date: 1991-04-04, close_len: 2, sma_s_len: 2  
date: 1991-04-05, close_len: 3, sma_s_len: 3  
date: 1991-04-08, close_len: 4, sma_s_len: 4  
date: 1991-04-09, close_len: 5, sma_s_len: 5  
len就都从1开始了。  
&emsp;&emsp;要获取某条线在内存中存储了多少个数据，要用线的方法buflen()。接上面修改next中的print如下：
```python
print("date: {}, close_len: {}, sma_s_len: {}".format(dt.isoformat(), (self.data.close.buflen()), (self.sma_s.buflen())))
```
date: 1991-04-03, close_len: 7124, sma_s_len: 7124  
date: 1991-04-04, close_len: 7124, sma_s_len: 7124  
date: 1991-04-05, close_len: 7124, sma_s_len: 7124  
date: 1991-04-08, close_len: 7124, sma_s_len: 7124  
date: 1991-04-09, close_len: 7124, sma_s_len: 7124  
date: 1991-04-10, close_len: 7124, sma_s_len: 7124  
可以看出，原始数据和指标的个数都是一样的，没有变化：7124。把计算指标的周期换成10，看看变化：  
date: 1991-04-18, close_len: 7124, sma_s_len: 7124  
date: 1991-04-19, close_len: 7124, sma_s_len: 7124  
date: 1991-04-23, close_len: 7124, sma_s_len: 7124  
date: 1991-04-24, close_len: 7124, sma_s_len: 7124  
date: 1991-04-25, close_len: 7124, sma_s_len: 7124  
除了输出日期变了外，其他没有变化。也就是说Backtrader会把指标缺失的数据补齐。  
&emsp;&emsp;next()方法里计算的数据是从周期个开始的，那前面数据怎么获得呢？Strategy里有两个函数可以获得：prenext()和nextstart()。周期达到之前，比如周期为10，在1到9都是在prenext里，第10个看情况，如果nextstart()实现了，即使是一个空函数，也会占用第十个数据(nextstart只调用一次)，如果没有实现，那就不占。prenext(), nextstart()和next()实现如下，其他不变，周期为10：
```python
def prenext(self):
    print('prenext')
    dt = self.datas[0].datetime.date(0)
    print("date: {}, close: {}, sma_s: {}".format(dt.isoformat(), self.data.close[0], self.sma_s[0]))

def nextstart(self):
    pass
    print('nextstart')
    dt = self.datas[0].datetime.date(0)
    print("date: {}, close: {}, sma_s: {}".format(dt.isoformat(), self.data.close[0], self.sma_s[0]))


def next(self):
    print('next')
    dt = self.datas[0].datetime.date(0)
    print("date: {}, close: {}, sma_s: {}".format(dt.isoformat(), self.data.close[0], self.sma_s[0]))
```
输出结果如下：  
prenext  
date: 1991-04-03, close: 0.491029, sma_s: nan  
prenext  
date: 1991-04-04, close: 0.48862396, sma_s: nan  
prenext  
date: 1991-04-05, close: 0.48621892, sma_s: nan  
prenext  
date: 1991-04-08, close: 0.48140884, sma_s: nan  
prenext  
date: 1991-04-09, close: 0.4790038, sma_s: nan  
prenext  
date: 1991-04-10, close: 0.47659876, sma_s: nan  
prenext  
date: 1991-04-12, close: 0.47178868, sma_s: nan  
prenext  
date: 1991-04-16, close: 0.46250136, sma_s: nan  
prenext  
date: 1991-04-17, close: 0.4602078, sma_s: nan  
nextstart  
date: 1991-04-18, close: 0.45791424, sma_s: 0.475529536  
next  
date: 1991-04-19, close: 0.45562068, sma_s: 0.471988704  
next  
date: 1991-04-23, close: 0.44649, sma_s: 0.46777530799999995  
next  
date: 1991-04-24, close: 0.44430716, sma_s: 0.463584132  
next  
date: 1991-04-25, close: 0.44212432, sma_s: 0.45965568  
next  
date: 1991-04-26, close: 0.43994148, sma_s: 0.455749448  
next  
date: 1991-04-29, close: 0.4355758, sma_s: 0.45164715199999994  
一共打印了9个prenext，也就是prenext执行了9次，补齐的数据为nan；nextstart执行了1次，后面就都是next。把nextstart里的实现换成pass，也就是空语句，啥都不干，看看会发生什么：  
prenext  
date: 1991-04-03, close: 0.491029, sma_s: nan  
prenext  
date: 1991-04-04, close: 0.48862396, sma_s: nan  
prenext  
date: 1991-04-05, close: 0.48621892, sma_s: nan  
prenext  
date: 1991-04-08, close: 0.48140884, sma_s: nan  
prenext  
date: 1991-04-09, close: 0.4790038, sma_s: nan  
prenext  
date: 1991-04-10, close: 0.47659876, sma_s: nan  
prenext  
date: 1991-04-12, close: 0.47178868, sma_s: nan  
prenext  
date: 1991-04-16, close: 0.46250136, sma_s: nan  
prenext  
date: 1991-04-17, close: 0.4602078, sma_s: nan  
next  
date: 1991-04-19, close: 0.45562068, sma_s: 0.471988704  
next  
date: 1991-04-23, close: 0.44649, sma_s: 0.46777530799999995  
next  
date: 1991-04-24, close: 0.44430716, sma_s: 0.463584132  
prnext还是有9个，nextstart没有，因为是空函数，后面都是next。但是丢失了一天的数据，本应该是要在nextstart里面处理的，丢失了。这表明，即使nextstart只是一个空函数，数据也会被当作处理，这点要特别注意。那我们试试把nextstart注释掉，不实现：  
prenext  
date: 1991-04-03, close: 0.491029, sma_s: nan  
prenext  
date: 1991-04-04, close: 0.48862396, sma_s: nan  
prenext  
date: 1991-04-05, close: 0.48621892, sma_s: nan  
prenext  
date: 1991-04-08, close: 0.48140884, sma_s: nan  
prenext  
date: 1991-04-09, close: 0.4790038, sma_s: nan  
prenext  
date: 1991-04-10, close: 0.47659876, sma_s: nan  
prenext  
date: 1991-04-12, close: 0.47178868, sma_s: nan  
prenext  
date: 1991-04-16, close: 0.46250136, sma_s: nan  
prenext  
date: 1991-04-17, close: 0.4602078, sma_s: nan  
next  
date: 1991-04-18, close: 0.45791424, sma_s: 0.475529536  
next  
date: 1991-04-19, close: 0.45562068, sma_s: 0.471988704  
next  
date: 1991-04-23, close: 0.44649, sma_s: 0.46777530799999995  
next  
date: 1991-04-24, close: 0.44430716, sma_s: 0.463584132   
prenext还是9个，后面就都是next，但是数据可以衔接上，没有丢失数据。  
&emsp;&emsp;这三个函数特性，在多支股票组合时，很有用。这个后面再讲。
