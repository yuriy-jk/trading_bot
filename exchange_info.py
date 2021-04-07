from api_data import api, secret
from bot_api import Binance

bot = Binance(API_KEY=api, API_SECRET=secret)

limits = bot.exchangeInfo()

tiker = 'AXSUSDT'

for elem in limits['symbols']:
    if elem['symbol'] == tiker:
        Tiker_limits = elem
        break
    else:
        raise Exception('Не удалось найти тикер' + tiker)
