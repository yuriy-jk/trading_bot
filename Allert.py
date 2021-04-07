from binance.client import Client
from api_data import api, secret
from talib._ta_lib import *
import numpy as np
import numpy
from datetime import datetime as dt

client = Client(api, secret)

open = []
high = []
low = []
close = []
volume = []


def indic_array(tiker):
    for kline in client.futures_klines(symbol=tiker, interval=client.KLINE_INTERVAL_1HOUR, limit=25):
    #for kline in client.futures_klines(symbol=tiker, interval=client.KLINE_INTERVAL_30MINUTE, limit=72):
        open.append(float(kline[1]))
        high.append(float(kline[2]))
        low.append(float(kline[3]))
        close.append(float(kline[4]))
        volume.append(float(kline[5]))


def allert_buy(tiker, period) -> object:
    indic_array(tiker)
    a, b = period
    # willr = WILLR(np.array(high), np.array(low), np.array(close), timeperiod=a)
    # aroondown, aroonup = AROON(np.array(high), np.array(low), timeperiod=b)
    sar = SAR(np.array(high), np.array(low), acceleration=a, maximum=b)
    if sar[-1] < open[-1]:
        print('Sar: {}, Open: {}'.format(sar[-1], open[-1]))
        #print('High: {}, Low: {}'.format(high[-1], low[-1]))
        return True
    else:
        print('Sar: {}, Open: {}'.format(sar[-1], open[-1]))
        #print('High: {}, Low: {}'.format(high[-1], low[-1]))


def allert_sell(tiker, period) -> object:
    indic_array(tiker)
    a, b = period
    # willr = WILLR(np.array(high), np.array(low), np.array(close), timeperiod=a)
    # aroondown, aroonup = AROON(np.array(high), np.array(low), timeperiod=b)
    sar = SAR(np.array(high), np.array(low), acceleration=a, maximum=b)
    if sar[-1] > open[-1]:
        print('Sar: {}, Open: {}'.format(sar[-1], open[-1]))
        #print('High: {}, Low: {}'.format(high[-1], low[-1]))
        return True
    else:
        print('Sar: {}, Open: {}'.format(sar[-1], open[-1]))
        #print('High: {}, Low: {}'.format(high[-1], low[-1]))



# sar = allert_buy('BTCUSDT', (21,14))
# print(list(sar)[-1])
# print(open[-1])
