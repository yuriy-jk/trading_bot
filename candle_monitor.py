from binance.client import Client
from datetime import datetime as dt
from api_data import api, secret
from Allert import volume_allert
import time

client = Client(api, secret)

time_res = client.get_server_time()  # server time
# print('server_time: {}'.format(dt.fromtimestamp(time_res['serverTime']/1000)))
# print('local_time: {}'.format(dt.now()))


while True:
    if dt.now().minute % 15 == 0 and dt.now().second == 0:
        volume_allert('AXSUSDT')
    else:
        pass




