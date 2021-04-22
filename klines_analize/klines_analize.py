from binance.client import Client
import csv
from api_data import api, secret

client = Client(api, secret)


def klines_to_csv_15(tiker):
    """функция для получения данных 15 минутных свечей по тикеру
    и записывающая в csv файл для последующего анализа"""
    data = []
    for kline in client.get_historical_klines_generator(tiker, Client.KLINE_INTERVAL_1HOUR, "1 month ago UTC"):
        data.append(kline)
        # write kline data to csv for analyse
        with open(tiker + '1h' + '1m' + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['time', 'open', 'high', 'low', 'close', 'vol']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in data:
                writer.writerow({'time': i[0], 'open': i[1], 'high': i[2], 'low': i[3], 'close': i[4],
                                 'vol': i[5]})
    return print('Csv file done')


tickers_base = ['BTCUSDT', 'ETHUSDT']
tickers = ['XRPUSDT', 'KNCUSDT', 'ICXUSDT', 'FTMUSDT', 'EOSUSDT', 'AXSUSDT', 'ADAUSDT', 'ALGOUSDT', 'ENJUSDT', 'HOTUSDT', 'VETUSDT', 'FLMUSDT']
for i in tickers_base:
    klines_to_csv_15(i)

