import ccxt
import os
import pandas as pd
import argparse
import logging

from ccxt import RequestTimeout

FORMAT = '%(name)s %(levelname)s %(asctime)s %(funcName)s  %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('GetDataFromBinance')


def get_exchange_data(_exchange_handler,
                      _coin_name, _time_period, _range_number,
                      _storage_path, _limit=500, _retry_times=5
                      ):
    """
    从交易所拉取特定币种交易对的一定时间范围内的数据

    Args:
        _exchange_handler:  交易所的handler
        _coin_name:     源币名
        _time_period:   时间长度
        _range_number:  获取轮数
        _storage_path:  下载好的数据存储路径
        _limit:     单次请求数据最大限制
        _retry_times:   重试次数

    Returns:

    """
    target_coin_name = 'USDT'
    coin_pair = f'{_coin_name}/{target_coin_name}'
    logger.debug(f'candidate coin pair:{coin_pair}')
    retrieved_data_list = []
    start_time = None
    logger.info('start download data')
    for i in range(_range_number):
        logger.info(f'start round {i + 1}')
        if start_time:
            logger.debug(f'start download from {start_time}')
        else:
            logger.debug('start download recent data')
        m_retry_times = _retry_times
        while m_retry_times:
            try:
                m_data = _exchange_handler.fetch_ohlcv(coin_pair,
                                                       timeframe=_time_period,
                                                       limit=_limit,
                                                       since=start_time)
                break
            except RequestTimeout as te:
                if m_retry_times:
                    m_retry_times -= 1
                    logger.debug(f'retry {_retry_times - m_retry_times}')
                    continue
                else:
                    raise te
        logger.debug(f'fetch {len(m_data)} records')
        if len(retrieved_data_list) == 0 or (retrieved_data_list and m_data[0][0] < retrieved_data_list[0][0]):
            retrieved_data_list = m_data + retrieved_data_list
        else:
            logger.info('reach head')
            break
        m_time_interval_between_records = m_data[1][0] - m_data[0][0]
        start_time = retrieved_data_list[0][0] - _limit * m_time_interval_between_records
    logger.info('finish download data')
    end_time = retrieved_data_list[-1][0]
    df = pd.DataFrame.from_records(retrieved_data_list, columns=["time", "open", "high", "low", "close", "vol"])
    df['time_stamp'] = pd.to_datetime(df["time"], unit="ms")
    df.drop_duplicates(subset=['time_stamp'], inplace=True)
    logger.debug(f'downloaded {len(df)} records of {coin_pair}')
    to_save_path = os.path.join(_storage_path, f'{_coin_name}_{target_coin_name}_{_time_period}')
    target_file_name = f'from_{start_time}_to_{end_time}.csv'
    target_file_full_path = os.path.join(to_save_path, target_file_name)
    logger.debug(f'save to {target_file_full_path}')
    os.makedirs(to_save_path, exist_ok=True)
    df.to_csv(target_file_full_path, index=False)
    logger.info(f'finish download data from {start_time} to {end_time} of {coin_pair}')


def main():
    ag = argparse.ArgumentParser('Get Data from Binance')
    ag.add_argument('--time_period', type=int, required=True, help='时间长度')
    ag.add_argument('--time_period_type', type=str, default='h',
                    choices=['y', 'M', 'w', 'd', 'h', 'm', 's'],
                    help='时间长度单位',
                    )
    ag.add_argument('--coin', '-c', nargs='+', type=str, required=True,
                    choices=[
                        "BTC", "ETH", "EOS", "FIL", "LTC",
                        "XRP", "DOT", "KSM", "CAKE", "BNB",
                        "ADA", "UNI", "SHIB"
                    ], help='需要下载的币的数据',
                    )
    ag.add_argument('--range_num', type=int, default=10, help='获取多少轮数据')
    ag.add_argument('--storage_path', type=str, default='./download_data', help='数据存储路径')
    ag.add_argument('--proxy', type=str, default=None, help='代理路径')
    ag.add_argument('--enable_debug_info', dest='debug', default=False, action='store_true', help='开启debug模式')

    args = ag.parse_args()
    if args.debug:
        logger.setLevel('DEBUG')
        logger.debug('start Debug mode')
    else:
        logger.setLevel('INFO')
        logger.info('start Info mode')
    exchange = ccxt.binance()
    if args.proxy:
        logger.info('start proxy mode')
        logger.debug(f'proxy:{args.proxy}')
        proxies = {
            'http': args.proxy,
            'https': args.proxy,
        }
        exchange.proxies = proxies
    logger.debug('exchange handler init finish')
    # 获取的K线的时间周期
    time_period = f"{args.time_period}{args.time_period_type}"
    logger.debug(f'time period:{time_period}')
    # 进行多少轮的数据获取
    range_number = args.range_num
    logger.debug(f'range number:{range_number}')
    # 每一轮获取到的数据(有些交易所的接口限制每次最多获取1000条数据）
    limit_number = 1000
    logger.debug(f'limit number:{limit_number}')
    storage_path = args.storage_path
    logger.debug(f'storage_path:{storage_path}')
    for m_coin_name in args.coin:
        logger.debug(f'start download {m_coin_name} data')
        get_exchange_data(exchange, m_coin_name, time_period, range_number, storage_path, limit_number, 5)


if __name__ == '__main__':
    main()
