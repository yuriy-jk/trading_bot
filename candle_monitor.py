from binance.client import Client
from datetime import datetime as dt
from api_data import api, secret
from Allert import allert_buy, allert_sell
import time

client = Client(api, secret)


def buy_signal(tiker, period):
    """проверка 1 час свечей на наличие сигнала на покупку"""
    while True:
        # запуск проверки кажды час
        # if dt.now().minute == 59 and dt.now().second == 58 and (10 > dt.now().microsecond > 0):
        if dt.now().minute == 0 and dt.now().second == 30:
            if allert_buy(tiker, period):
                # print('server_time: {}'.format(dt.fromtimestamp(client.get_server_time()['serverTime'] / 1000)))
                # print('local_time: {}'.format(dt.now()))
                print('Buy!')
                return True
            else:
                # print('server_time: {}'.format(dt.fromtimestamp(client.get_server_time()['serverTime'] / 1000)))
                # print('local_time: {}'.format(dt.now()))
                # print('Not yet!')
                time.sleep(3580)
                pass
        else:
            pass


def sell_signal(tiker, period):
    """проверка 1 час свечей на наличие сигнала на продажу"""
    while True:
        # запуск проверки каждые 15 минут
        # if dt.now().minute == 59 and dt.now().second == 58 and (10 > dt.now().microsecond > 0):
        if dt.now().minute == 0 and dt.now().second == 30:
            if allert_sell(tiker, period):
                # print('server_time: {}'.format(dt.fromtimestamp(client.get_server_time()['serverTime'] / 1000)))
                # print('local_time: {}'.format(dt.now()))
                print('Sell!')
                return True
            else:
                # print('server_time: {}'.format(dt.fromtimestamp(client.get_server_time()['serverTime'] / 1000)))
                # print('local_time: {}'.format(dt.now()))
                # print('Not yet!')
                time.sleep(3580)
                pass
        else:
            pass
