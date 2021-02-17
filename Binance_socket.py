from binance.websockets import BinanceSocketManager
from binance.client import Client
from binance.enums import *


def process_message(msg):
    if msg['e'] == 'error':
        bm.stop_socket(conn_key)
    else:
        print('message type: {}'.format((msg['e'])))
        print(msg)


api = 'eUI2ooXokT9pZhfg1xv839MK0uK2uitJQIf1sd5XmsBYwFZayJfMeNqgvZKpKGZC'
secret = '9mBWXsKji44XEoztbF3h2fd2E94C9spoDZz11Q2ql27SE3oehfSjrnhzr2inGrgP'
client = Client(api, secret)

bm = BinanceSocketManager(client, user_timeout=3)

conn_key = bm.start_kline_socket('BNBUSDT', process_message, interval=KLINE_INTERVAL_30MINUTE)

bm.start()

