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
    path = Path(str(now) + tiker)
    path.mkdir()
    file_name = tiker + timeframe + '1m' + '.csv'
    file_path = os.path.join(path, file_name)
    print(file_path)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['time', 'open', 'high', 'low', 'close', 'vol']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow({'time': i[0], 'open': i[1], 'high': i[2], 'low': i[3], 'close': i[4],
                            'vol': i[5]})
    csv_name = tiker + timeframe + '1m' + '.csv'
    # print('Csv file done')
    return str('main/' + file_path)


f_klines_to_csv('ONEUSDT', '1HOUR')