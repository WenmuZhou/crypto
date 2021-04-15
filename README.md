# crypto

用于数字货币的量化交易

## linux install ta_lib

### 安装ta-lib源码

```
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz #下载
    tar -xvf ta-lib-0.4.0-src.tar.gz  # 解压
    cd ta-lib # 进入目录
    ./configure --prefix=/usr
    make
    make install
```

### 安装python版本的ta_lib
```
    git clone https://github.com/mrjbq7/ta-lib.git
    cd ta-lib
    python setup.py install
```

### 解决bug

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