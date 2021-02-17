from binance.client import Client
import csv
from api_data import api, secret

client = Client(api, secret)


def klines_to_csv_15(tiker):
    """функция для получения данных 15 минутных свечей по тикеру
    и записывающая в csv файл для последующего анализа"""
    data = []
    for kline in client.get_historical_klines_generator(tiker, Client.KLINE_INTERVAL_15MINUTE, "1 week ago UTC"):
        data.append(kline)
        # write kline data to csv for analyse
        with open(tiker + '15m' + '1w' + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['time', 'open', 'high', 'low', 'close', 'vol', 'taker_vol', 'price_delta']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in data:
                delta = float(i[4]) - float(i[1])
                writer.writerow({'time': i[0], 'open': i[1], 'high': i[2], 'low': i[3], 'close': i[4],
                                 'vol': i[5], 'taker_vol': i[9], 'price_delta': delta})
    return print('Csv file done')


klines_to_csv_15('AXSUSDT')







