from candle_monitor import buy_signal, sell_signal
from bot_api import Binance
from api_data import api, secret
from binance.client import Client
from datetime import datetime as dt
import time

client = Client(api, secret)

bot = Binance(API_KEY=api, API_SECRET=secret)
limits = bot.futuresExchangeInfo()
tiker = 'ONEUSDT'

# получаем лимиты по тикеру
Tiker_limits = []
for elem in limits['symbols']:
    if elem['symbol'] == tiker:
        Tiker_limits = elem
        break


# Ф-ция, которая приводит любое число к числу, кратному шагу, указанному биржей
# Если передать параметр increase=True то округление произойдет к следующему шагу
def adjust_to_step(value, step, increase=False):
   return ((int(value * 100000000) - int(value * 100000000) % int(
        float(step) * 100000000)) / 100000000)+(float(step) if increase else 0)


# данные для индикатора
acceleration = 0.2
maximum = 0.2
indic_period = (acceleration, maximum)

# данные для ордеров
long = False
short = False
quantity = 0

# sleep до начала нового часа
wait_time = ((60 - dt.now().minute) * 60) - dt.now().second
time.sleep(wait_time)

while True:
    if long:
        # получаем сигнал на продажу
        if sell_signal(tiker, indic_period):
            if long:
                # создаем ордер close long
                long_close_order = client.futures_create_order(
                    symbol=tiker,
                    side='SELL',
                    positionSide='BOTH',
                    type='MARKET',
                    recvWindow=5000,
                    quantity=quantity
                )
                print('Close-Long Order done')
                long = False
            if not short:
                # создаем ордер на продажу
                # расчитываем данные для ордера
                orders = client.futures_order_book(symbol=tiker, limit=5)  # последние 5 ордеров
                price = orders['bids'][0][0]  # ближайший ордер на покупку
                quantity = adjust_to_step(100 / float(price), Tiker_limits['filters'][2]['stepSize'])  # кол монет на 100$
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
                time.sleep(3580)
    if not long:
        # получаем сигнал на покупку
        if buy_signal(tiker, indic_period):
            if short:
                # создаем ордер close short
                short_close_order = client.futures_create_order(
                    symbol=tiker,
                    side='BUY',
                    positionSide='BOTH',
                    type='MARKET',
                    recvWindow=5000,
                    quantity=quantity
                )
                print('Short-Close Order done')
                short = False
            # создаем ордер на покупку
            # расчитываем данные для ордера
            if not long:
                orders = client.futures_order_book(symbol=tiker, limit=5)  # последние 5 ордеров
                price = orders['asks'][0][0]  # ближайший ордер на продажу
                quantity = adjust_to_step(100 / float(price), Tiker_limits['filters'][2]['stepSize'])  # кол монет на 100$
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
                time.sleep(3580)








