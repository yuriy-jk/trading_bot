from candle_monitor import buy_signal
from api_data import api, secret
from bot_api import Binance
import json

#volume_allert('AXSUSDT')

bot = Binance(API_KEY=api, API_SECRET=secret)

#print(bot.account())

buy_signal('AXSUSDT')
