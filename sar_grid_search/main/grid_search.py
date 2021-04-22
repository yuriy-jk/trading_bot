import csv
import os
from pathlib import Path
from datetime import datetime as dt
import numpy as np
import pandas as pd
from binance.client import Client
from talib._ta_lib import *

from api_data import api, secret

client = Client(api, secret)


def f_klines_to_csv(tiker, timeframe):
    """функция для получения данных свечей по тикеру
    и записывающая в csv файл для последующего анализа"""
    data = []
    if timeframe == '30MINUTE':
        for kline in client.futures_klines(symbol=tiker, interval=client.KLINE_INTERVAL_30MINUTE, limit=1440):
            data.append(kline)
            # write kline data to csv for analyse
    if timeframe == '1HOUR':
        for kline in client.futures_klines(symbol=tiker, interval=client.KLINE_INTERVAL_1HOUR, limit=720):
            data.append(kline)
            # write kline data to csv for analyse
    if timeframe == '4HOUR':
        for kline in client.futures_klines(symbol=tiker, interval=client.KLINE_INTERVAL_4HOUR, limit=180):
            data.append(kline)
            # write kline data to csv for analyse
    now = dt.now().date()
    file_name = tiker + timeframe + '1m' + '.csv'
    path = Path(str(now) + tiker + '/')
    if os.path.exists(path):
        pass
    else:
        path.mkdir()
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['time', 'open', 'high', 'low', 'close', 'vol']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow({'time': i[0], 'open': i[1], 'high': i[2], 'low': i[3], 'close': i[4],
                            'vol': i[5]})
    return str(file_path)


def Indicators_sar_test(df, indics):
    a, b = indics
    volume = df.vol
    open = df.open
    close = df.close
    high = df.high
    low = df.low
    sar = SAR(high, low, maximum=a, acceleration=b)
    df = df.join(pd.DataFrame(
                {
                    'sar': sar,
                }))
    return df


def profit_base_long(df):
    open_long = []
    close_long = []
    sar = df.sar
    open = df.open
    buy = False
    for i in range(1, (len(open)-1)):
        if buy:
            if sar[i] > open[i]:
                close_long.append(open[i+1])
                buy = False
        else:
            if sar[i] < open[i]:
                open_long.append(open[i+1])
                buy = True
    pnl_buy = pd.DataFrame({'open_long': open_long})
    pnl_sell = pd.DataFrame({'close_long': close_long})
    pnl = pnl_buy.join(pnl_sell)
    pnl = pnl.dropna()
    return pnl


def profit_base_short(df):
    open_short = []
    close_short = []
    sar = df.sar
    open = df.open
    sell = False
    for i in range(1, (len(open)-1)):
        if sell:
            if sar[i] < open[i]:
                close_short.append(open[i+1])
                sell = False
        else:
            if sar[i] > open[i]:
                open_short.append(open[i+1])
                sell = True
    pnl_buy = pd.DataFrame({'open_short': open_short})
    pnl_sell = pd.DataFrame({'close_short': close_short})
    pnl = pnl_buy.join(pnl_sell)
    pnl = pnl.dropna()
    return pnl


def testing_long(df):
    m = 50
    y = 0
    for index, row in df.iterrows():
        y = (100 / row[0]) * row[1]
        if y > 100:
            x = y - 100
            m += x
        if y < 100:
            delta = 100 - y
            m -= delta
    return m + y


def testing_short(df):
    m = 50
    y = 0
    for index, row in df.iterrows():
        profit = ((100/row[1]) - (100/row[0])) * row[1]
        y = profit + 100
        if y > 100:
            x = y - 100
            m += x
        if y < 100:
            delta = 100 - y
            m -= delta
    return m + 100


def grid_search(csv_data):
    data = pd.read_csv(str(csv_data))
    data['time'] = pd.to_datetime(data.time, unit='ms')
    data.index = data.time
    data = data.drop(columns='time')
    a = list(np.arange(0.001, 0.01, 0.001))
    b = list(np.arange(0.01, 0.1, 0.01))
    c = [0.1, 0.2]
    order_acc = a + b + c
    order_max = np.arange(0.1, 0.2, 0.01)
    best_res = 0
    best_order = ()
    for a in order_acc:
        for b in order_max:
            indics = (a, b)
            data_i = Indicators_sar_test(data, indics)
            data_i = data_i.dropna()
            pnl_long = profit_base_long(data_i)
            res_long = testing_long(pnl_long)
            pnl_short = profit_base_short(data_i)
            res_short = testing_short(pnl_short)
            res = res_long + res_short
            if res > best_res:
                best_res = res
                best_order = indics
    return print('Best_order: {} - Best_Res: {}'.format(best_order, best_res))







