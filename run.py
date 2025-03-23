"""
В этом файле выполняются такие задачи:

1. Чтение файла config.json с последующим получением токена и флага логирования
2. Создание объекта класса aiogram.Bot и запуск бота через диспетчер с роутером из файла handlers
3. Условие __name__ == '__main__' после которого идёт проверка на логирование и последующая
попытка запуска корутины main()
"""
import asyncio
import json
import logging

from aiogram import Bot, Dispatcher

from app.handlers import router

# Получение конфига и запись его в переменную config
with open('config.json') as file:
    config = json.load(file)

# Создание объекта класса Bot с токеном из конфига и введение диспетчера в переменной dp
bot = Bot(token=config['TOKEN'])
dp = Dispatcher()


# Объявление корутины запуска с диспетчером
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


# Условие для запуска программы в основном файле и включение логирования через конфиг
if __name__ == '__main__':
    if config['LOGGING']:
        logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
