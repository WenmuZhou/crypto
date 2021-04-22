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

## 3、线上交易部分(trading)

### 3.1 trade_execution

本部分代码主要用于策略的线上自动执行部分代码。<br>
根据不同的执行时间周期进行策略的划分。

### 3.2 trade_strategy

本部分代码主要用于策略算法的编写。<br>
策略执行的基本逻辑在`base_trading.py`中定义好了基本策略执行逻辑。<br>
定义新的策略只需要继承`BasisTrading`类，重写`strategy_trade`方法即可。<br>
示例代码：`two_ma.py`


