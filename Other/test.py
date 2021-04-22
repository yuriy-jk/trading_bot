from candle_monitor import buy_signal, sell_signal
from functions import *
from api_data import api, secret
from binance.client import Client
from datetime import datetime as dt
import time

client = Client(api, secret)

tiker = 'ONEUSDT'
quantity = 5

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
    print('done')
except:
    pass
