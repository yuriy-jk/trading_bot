from binance.client import Client
from api_data import api, secret
import numpy
from datetime import datetime as dt

client = Client(api, secret)


def percentile(tiker):
    """функция считает перцентиль 4х показателей 15 минутных свечей за последнюю неделю"""
    vol, vol_delta, taker_vol, price_delta = [], [], [], []
    vol_50, vol_delta_25, taker_vol_50, price_delta_50 = None, None, None, None
    # получаем данные 15 минутных свечей за неделю
    for kline in client.get_historical_klines_generator(tiker, Client.KLINE_INTERVAL_15MINUTE, "1 week ago UTC"):
        vol.append(float(kline[5]))
        delta = float(kline[9]) - (float(kline[5]) / 2)
        vol_delta.append(delta)
        taker_vol.append(float(kline[9]))
        price = float(kline[4]) - float(kline[1])
        price_delta.append(price)
        # считаем показатели перцентилей
        vol_50, vol_delta_25, taker_vol_50, price_delta_50 = numpy.percentile(vol, [50])[0], \
                                                             numpy.percentile(vol_delta, [25])[0], \
                                                             numpy.percentile(taker_vol, [50])[0], \
                                                             numpy.percentile(price_delta, [50])[0]
    return vol_50, vol_delta_25, taker_vol_50, price_delta_50


def volume_allert(tiker):
    """функция получает данные последней 15минутной свечи и сравнивает показатели свечи с высчитанными перцентилями"""
    vol_50, vol_delta_25, taker_vol_50, price_delta_50 = percentile(tiker)
    # получаем данные 15м свечи
    kline = client.get_klines(symbol=tiker, interval=client.KLINE_INTERVAL_15MINUTE, limit=1)[0]
    #open, close = dt.fromtimestamp(int(kline[0] / 1000)), dt.fromtimestamp(int(kline[6]) / 1000)
    vol = float(kline[5])
    vol_delta = float(kline[9]) - (float(kline[5]) / 2)
    taker_vol = float(kline[9])
    price_delta = float(kline[4]) - float(kline[1])
    mean_price = (float(kline[1]) + float(kline[4])) / 2
    # сравниваем данные, получаем сигнал на покупку
    if vol > vol_50 and vol_delta < vol_delta_25 and taker_vol < taker_vol_50 and price_delta < price_delta_50:
        print(open)
        print('BUUUY!')
        print(mean_price)
        return True
    else:
        print(open)
        print(mean_price)
        return False

