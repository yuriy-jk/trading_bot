from binance.client import Client
from api_data import api, secret
import numpy
from datetime import datetime as dt
import time

client = Client(api, secret)


def percentile(tiker):
    """функция считает 75 перцентиль положительной
    дельты от обьемов на покупку к общему обьему"""
    vol, vol_delta, taker_vol, price_delta = [], [], [], []
    vol_50, vol_delta_25, taker_vol_50, price_delta_50 = None, None, None, None
    for kline in client.get_historical_klines_generator(tiker, Client.KLINE_INTERVAL_15MINUTE, "1 week ago UTC"):
        vol.append(float(kline[5]))
        delta = float(kline[9]) - (float(kline[5]) / 2)
        vol_delta.append(delta)
        taker_vol.append(float(kline[9]))
        price = float(kline[4]) - float(kline[1])
        price_delta.append(price)
        vol_50, vol_delta_25, taker_vol_50, price_delta_50 = numpy.percentile(vol, [50])[0], \
                                                             numpy.percentile(vol_delta, [25])[0], \
                                                             numpy.percentile(taker_vol, [50])[0], \
                                                             numpy.percentile(price_delta, [50])[0]
    return vol_50, vol_delta_25, taker_vol_50, price_delta_50


def volume_allert(tiker):
    """'"""
    vol_50, vol_delta_25, taker_vol_50, price_delta_50 = percentile(tiker)
    kline = client.get_klines(symbol=tiker, interval=client.KLINE_INTERVAL_15MINUTE, limit=1)[0]
    # print(kline)
    open, close = dt.fromtimestamp(int(kline[0] / 1000)), dt.fromtimestamp(int(kline[6]) / 1000)
    vol = float(kline[5])
    vol_delta = float(kline[9]) - (float(kline[5]) / 2)
    taker_vol = float(kline[9])
    price_delta = float(kline[4]) - float(kline[1])
    mean_price = (float(kline[1]) + float(kline[4])) / 2

    if vol > vol_50 and vol_delta < vol_delta_25 and taker_vol < taker_vol_50 and price_delta < price_delta_50:
        print(open)
        print('BUUUY!')
        print(mean_price)
        return True
    # print(f'Allert,\n\
    # Open_15min_candle: {open},\n\
    # Delta: {delta}\n\

    # Mean_price: %.3f\n\
    # Open_price: %.3f\n\
    # Close_price: %.3f\n\
    # Max_price: %.3f\n\
    # Min_price: %.3f\n' % (mean_price, float(kline[1]), float(kline[4]), float(kline[2]), float(kline[3])))
    else:
        print(open)
        print(mean_price)
        return False
    # print(f'Open_15min_candle: {open},\n\
    # Delta: {delta}\n\
    # Mean_price: %.3f\n\
    # Open_price: %.3f\n\
    # Close_price: %.3f\n\
    # Max_price: %.3f\n\
    # Min_price: %.3f\n' % (mean_price, float(kline[1]), float(kline[4]), float(kline[2]), float(kline[3])))
    # time.sleep(900)
