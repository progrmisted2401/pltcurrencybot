"""
В этом файле есть такие функции:

1. get_actual_currency(): Получение актуальных курсов валют на текущую дату с использованием библиотеки pycbrf.
2. get_currency_codes(): Получение списка кодов валют, доступных на текущую дату.
3. get_rate(): Получение курса конкретной валюты на указанную дату.
4. plot_currency_rate(): Построение графика изменения курса валюты за указанный период с использованием
библиотеки matplotlib с последующим возвращением графика в виде байтов для отправки в Telegram.
"""
import io
from datetime import timedelta, datetime

import matplotlib.pyplot as plt
from pycbrf import ExchangeRates


def get_actual_currency():
    # Возвращает актуальные курсы валют на текущую дату
    return ExchangeRates(str(datetime.now())[:10]).rates


def get_currency_codes() -> list[str]:
    # Возвращает список кодов валют (Например [USD, EUR]), доступных на текущую дату
    return [i.code for i in ExchangeRates(str(datetime.now())[:10]).rates]


async def get_rate(currency_type: str, date) -> float:
    # Возвращает курс валюты на указанную дату
    try:
        rates = ExchangeRates(date.strftime('%Y-%m-%d'))
        result = list(filter(lambda el: el.code == currency_type.upper(), rates.rates))[0]
        return float(result.rate)
    except Exception:
        raise Exception('The name of the currency is entered incorrectly.')


async def plot_currency_rate(currency, start_date, end_date):
    # Строит график курса валюты за указанный период и возвращает его в виде байтов
    dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    values = [await get_rate(currency, date) for date in dates]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, color='blue')
    plt.title(f'Курс {currency} за период с {start_date.strftime("%Y-%m-%d")} по {end_date.strftime("%Y-%m-%d")}')
    plt.xlabel('Дата')
    plt.ylabel('Курс (RUB)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()
