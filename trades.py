from main.candle_monitor import buy_signal, sell_signal
from main.Allert import side_signal
from main.functions import *

from api_data import api, secret
from binance.client import Client
from datetime import datetime as dt
import time

client = Client(api, secret)

tiker = 'ONEUSDT'

# получаем лимиты по тикеру
tik_limits = get_limits(tiker)

# данные для индикатора
acceleration = 0.02
maximum = 0.2
indic_period = (acceleration, maximum)

# take profits in %
tp1, tp2, tp3 = 5, 10, 15

# sleep до начала нового часа
wait_time = ((60 - dt.now().minute) * 60) - dt.now().second
time.sleep(wait_time)

# данные для ордеров
long = False
short = False
quantity = 0

# проверка индикатора для начальной позиции
if side_signal(tiker, indic_period) == 'Waiting_short':
    long = True
    print('wait_for short')
if side_signal(tiker, indic_period) == 'Waiting_long':
    short = True
    print('wait for long')

# запуск цикла
while True:
    if long:
        # получаем сигнал на продажу
        if sell_signal(tiker, indic_period):
            if long:
                # создаем ордер close long
                try:
                    long_close_order = client.futures_create_order(
                        symbol=tiker,
                        side='SELL',
                        positionSide='BOTH',
                        type='MARKET',
                        quantity=quantity,
                        reduceOnly='true',
                        recvWindow=5000,
                    )
                    print('Close-Long Order done')
                    long = False
                except:
                    pass
                    long = False
            if not short:
                # создаем ордер на продажу
                # расчитываем данные для ордера
                orders = client.futures_order_book(symbol=tiker, limit=5)  # последние 5 ордеров
                price = orders['bids'][0][0]  # ближайший ордер на покупку
                quantity = adjust_to_step(100 / float(price), tik_limits['filters'][2]['stepSize'])  # кол монет на 100$
                # создаем ордер open short
                sell_order = client.futures_create_order(
                    symbol=tiker,
                    side='SELL',
                    positionSide='BOTH',
                    type='MARKET',
                    recvWindow=5000,
                    quantity=quantity
                )
                print('Short Order done')
                short = True
                # создаем take_profit ордера
                short_tp_1 = client.futures_create_order(
                    symbol=tiker,
                    side='BUY',
                    positionSide='BOTH',
                    type='LIMIT',
                    reduceOnly='true',
                    price=round(float(price) - ((float(price) / 100) * tp1), 4),
                    quantity=round(((quantity / 100) * 25), 0),
                    recvWindow=5000,
                    timeInForce='GTC'
                )
                short_tp_2 = client.futures_create_order(
                    symbol=tiker,
                    side='BUY',
                    positionSide='BOTH',
                    type='LIMIT',
                    reduceOnly='true',
                    price=round(float(price) - ((float(price) / 100) * tp2), 4),
                    quantity=round(((quantity / 100) * 25), 0),
                    recvWindow=5000,
                    timeInForce='GTC'
                )
                short_tp_3 = client.futures_create_order(
                    symbol=tiker,
                    side='BUY',
                    positionSide='BOTH',
                    type='LIMIT',
                    reduceOnly='true',
                    price=round(float(price) - ((float(price) / 100) * tp3), 4),
                    quantity=round(((quantity / 100) * 25), 0),
                    recvWindow=5000,
                    timeInForce='GTC'
                )
                time.sleep(3580)
    if short:
        # получаем сигнал на покупку
        if buy_signal(tiker, indic_period):
            if short:
                # создаем ордер close short
                try:
                    short_close_order = client.futures_create_order(
                        symbol=tiker,
                        side='BUY',
                        positionSide='BOTH',
                        quantity=quantity,
                        reduceOnly='true',
                        type='MARKET',
                        recvWindow=5000,
                    )
                    print('Short-Close Order done')
                    short = False
                except:
                    pass
                    short = False
            # создаем ордер на покупку
            # расчитываем данные для ордера
            if not long:
                orders = client.futures_order_book(symbol=tiker, limit=5)  # последние 5 ордеров
                price = orders['asks'][0][0]  # ближайший ордер на продажу
                quantity = adjust_to_step(100 / float(price), tik_limits['filters'][2]['stepSize'])  # кол монет на 100$
                # создаем ордер open long
                buy_order = client.futures_create_order(
                    symbol=tiker,
                    side='BUY',
                    positionSide='BOTH',
                    type='MARKET',
                    recvWindow=5000,
                    quantity=quantity
                )
                print('Long Order done')
                long = True
                # создаем take_profit ордера
                long_tp_1 = client.futures_create_order(
                    symbol=tiker,
                    side='SELL',
                    positionSide='BOTH',
                    type='LIMIT',
                    reduceOnly='true',
                    price=round(float(price) + ((float(price) / 100) * tp1), 4),
                    quantity=round(((quantity / 100) * 25), 0),
                    recvWindow=5000,
                    timeInForce='GTC'
                )
                long_tp_2 = client.futures_create_order(
                    symbol=tiker,
                    side='SELL',
                    positionSide='BOTH',
                    type='LIMIT',
                    reduceOnly='true',
                    price=round(float(price) + ((float(price) / 100) * tp2), 4),
                    quantity=round(((quantity / 100) * 25), 0),
                    recvWindow=5000,
                    timeInForce='GTC'
                )
                long_tp_3 = client.futures_create_order(
                    symbol=tiker,
                    side='SELL',
                    positionSide='BOTH',
                    type='LIMIT',
                    reduceOnly='true',
                    price=round(float(price) + ((float(price) / 100) * tp3), 4),
                    quantity=round(((quantity / 100) * 25), 0),
                    recvWindow=5000,
                    timeInForce='GTC'
                )
                time.sleep(3580)
