import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class CurrencyConverter:

    @staticmethod
    def exceptions(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException('Одинаковые валюты не могут быть использованы для перевода')
        try:
           quote in keys[quote]
        except KeyError:
            raise ConvertionException(f'Валюта {quote} не опознана. Список доступных валют: /values')
        try:
            base in keys[base]
        except KeyError:
            raise ConvertionException(f'Валюта {base} не опознана. Список доступных валют: /values')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Сумма для конвертации должна быть представлена числом')
        r = requests.get(f'https://v6.exchangerate-api.com/v6/163321a501c82131caec215e/pair/{keys[quote]}/{keys[base]}')
        return r