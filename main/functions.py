from api_data import api, secret
from binance.client import Client


# Ф-ция, которая приводит любое число к числу, кратному шагу, указанному биржей
# Если передать параметр increase=True то округление произойдет к следующему шагу
def adjust_to_step(value, step, increase=False):
    return ((int(value * 100000000) - int(value * 100000000) % int(
        float(step) * 100000000)) / 100000000) + (float(step) if increase else 0)


client = Client(api, secret)


# функция, которая получает лимиты по тикеру
def get_limits(tiker):
    limits = []
    limits_from_bin = client.futures_exchange_info()
    for elem in limits_from_bin['symbols']:
        if elem['symbol'] == tiker:
            limits = elem
            break
    return limits



