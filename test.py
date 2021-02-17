from Allert import volume_allert
from api_data import api, secret
from trades import Binance
import json

#volume_allert('AXSUSDT')

bot = Binance(API_KEY=api, API_SECRET=secret)

#print(bot.account())

