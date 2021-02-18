from candle_monitor import buy_signal
from bot_api import Binance
from api_data import api, secret

bot = Binance(API_KEY=api, API_SECRET=secret)
tiker = 'AXSUSDT'


while True:
    # получаем сигнал на покупку
    if buy_signal(tiker):
        # создаем ордер на покупку
        new_order = bot.createOrder(
            symbol=tiker,
            recvWindow=5000,
            side='BUY',
            type='MARKET'
            quantity=
        )

