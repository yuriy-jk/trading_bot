# from candle_monitor import buy_signal, sell_signal
# from bot_api import Binance
# from api_data import api, secret
# from binance.client import Client
#
# client = Client(api, secret)
#
# tiker = 'EOSUSDT'
#
# def adjust_to_step(value, step, increase=False):
#     return ((int(value * 100000000) - int(value * 100000000) % int(
#         float(step) * 100000000)) / 100000000) + (float(step) if increase else 0)
#
#
# price_book = client.futures_order_book(symbol=tiker, limit=5)
# print(price_book['bids'])
# print(price_book['asks'])
# print(price_book['asks'][0][0])
# value = 100 / float(price_book['asks'][0][0])
# print(value)
#
# limits = client.futures_exchange_info()
# Tiker_limits = []
#
# # получаем лимиты по тикеру
# for elem in limits['symbols']:
#     if elem['symbol'] == tiker:
#         Tiker_limits = elem
#         break
#     # else:
#     #     raise Exception('Не удалось найти тикер: ' + tiker)
#
# print(Tiker_limits)
# print(Tiker_limits['filters'][2]['stepSize'])
# print(adjust_to_step(value, Tiker_limits['filters'][2]['stepSize']))
#
#
# orders = client.futures_order_book(symbol=tiker, limit=5)  # последние 5 ордеров
# price = orders['asks'][0][0]  # ближайший ордер на продажу
# quantity = adjust_to_step(100/float(price), Tiker_limits['filters'][2]['stepSize'])  # кол монет на 100$
#
# # создаем ордер на покупку
# new_order = client.futures_create_order(
#                 symbol=tiker,
#                 side='BUY',
#                 positionSide='BOTH',
#                 type='MARKET',
#                 recvWindow=5000,
#                 quantity=quantity
#             )
# print('New Order done')

from datetime import datetime as dt


# wait_min = (60 - dt.now().minute) * 60
# wait_sec = dt.now().second
# wait_time = wait_min + wait_sec


wait_time = ((60 - dt.now().minute) * 60) - dt.now().second
print(wait_time)
