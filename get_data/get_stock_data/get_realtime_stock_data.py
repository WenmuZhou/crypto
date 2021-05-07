import pandas as pd
import baostock as bs
import datetime

import tushare as ts

# def cb_func(ResultData):
#     print(ResultData)
#     for key in ResultData.data:
#         datestr = '%d-%02d-%02d %02d:%02d:%02d' % (date.year, date.month, date.day, date.hour, date.minute, date.second)
#         msg1 = {'method':"Sock.RealData", 'Code':ResultData.data[key][2][3:], 'Price':ResultData.data[key][6], 'Time':datestr, 'PriceYes':ResultData.data[key][5]}
#         print(msg1)

# if __name__ == '__main__':
#     login_ret = bs.login_real_time()

#     rs = bs.subscribe_by_code("sz.002236,sz.002415", 0, cb_func, "", "user_params")
#     if rs.error_code != '0':
#         print("request real time error", rs.error_msg)
#     else:
#         # 使主程序不再向下执行。使用time.sleep()等方法也可以
#         text = input("press any key to cancel real time \r\n")
#         # 取消订阅
#         cancel_rs = bs.cancel_subscribe(rs.serial_id)
#     # 登出
#     login_ret = bs.logout_real_time()

df = ts.get_realtime_quotes('000581')
print(df)
