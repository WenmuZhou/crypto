# import easyquotation

# quotation = easyquotation.use('sina')
# print(quotation)

import baostock as bs
import pandas as pd
import datetime

# 是否删除停盘数据
DROP_SUSPENSION = True

def update_stk_list(date = None):
    # 获取指定日期的指数、股票数据
    stock_rs = bs.query_all_stock(date)
    stock_df = stock_rs.get_data()
    stock_df.to_csv('F://all_list.csv', encoding = 'gbk', index = False)
    stock_df.drop(stock_df[stock_df.code < 'sh.600000'].index, inplace = True)
    stock_df.drop(stock_df[stock_df.code > 'sz.399000'].index, inplace = True)
    stock_df = stock_df['code']
    stock_df.to_csv('F://stk_list.csv', encoding = 'gbk', index = False)
    return stock_df.tolist()

def load_stk_list():
    df = pd.read_csv('F://stk_list.csv')
    return df['code'].tolist()

def convert_time(t):
    H = t[8:10]
    M = t[10:12]
    S = t[12:14]
    return H + ':' + M + ':' + S


def download_data(stk_list = [], fromdate = '1990-12-19', todate = datetime.date.today(), 
                   datas = 'date,open,high,low,close,volume,amount,turn,pctChg', 
                   frequency = 'd', adjustflag = '1'):
    for code in stk_list:
        print("Downloading :" + code)
        k_rs = bs.query_history_k_data_plus(code, datas, start_date = fromdate, end_date = todate.strftime('%Y-%m-%d'),
                                            frequency = frequency, adjustflag = adjustflag)
        datapath = 'F://stock_data//' + frequency + '/' + code + '.csv'
        out_df = k_rs.get_data()
        if DROP_SUSPENSION and 'volume' in list(out_df):
            out_df.drop(out_df[out_df.volume == '0'].index, inplace = True)
        # 做time转换
        if frequency in ['5', '15', '30', '60'] and 'time' in list(out_df):
            out_df['time'] = out_df['time'].apply(convert_time)
        out_df.to_csv(datapath, encoding = 'gbk', index = False)

if __name__ == '__main__':
    
    bs.login()

    # 首次运行
    # stk_list = update_stk_list(datetime.date.today() - datetime.timedelta(days = 31))
    # 非首次运行
    stk_list = load_stk_list()

    # 下载日线
    download_data(stk_list, datas = 'date,open,high,low,close,volume,amount,turn,pctChg,adjustflag')
    # 下载周线
    # download_data(stk_list, frequency = 'w')
    # # 下载月线
    # download_data(stk_list, frequency = 'm')
    # # 下载5分钟线
    # download_data(stk_list, frequency = '5', datas = 'date,time,open,high,low,close,volume,amount,adjustflag')
    # # 下载15分钟线
    # download_data(stk_list, fromdate = '2020-6-1', frequency = '15', datas = 'date,time,open,high,low,close,volume,amount,adjustflag')
    # # 下载30分钟线
    # download_data(stk_list, fromdate = '2020-6-1', frequency = '30', datas = 'date,time,open,high,low,close,volume,amount,adjustflag')
    # # 下载60分钟线
    # download_data(stk_list, fromdate = '2020-6-1', frequency = '60', datas = 'date,time,open,high,low,close,volume,amount,adjustflag')
    bs.logout()


