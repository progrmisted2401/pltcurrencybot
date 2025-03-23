"""
В этом файле есть такие функции:

1. cmd_start(): Обработка команды /start, которая отправляет приветственное сообщение и клавиатуру с выбором валюты.
2. get_currency(): Обработка выбора валюты пользователем, построение графика курса за последний месяц и отправка
его пользователю.
3. back(): Обработка кнопки "Назад", которая возвращает пользователя к выбору валюты.

В функциях выполняется логирование ошибок и предупреждений, связанных с обработкой сообщений и callback-запросов.
"""
import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, BufferedInputFile

import app.keyboards as kb
from app.currency_rate import plot_currency_rate, get_currency_codes, get_actual_currency

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    # Обработчик команды /start, отправляет приветственное сообщение и клавиатуру с выбором валюты
    await message.answer_sticker(sticker="CAACAgIAAxkBAAILImMls3AztJgD37K6ITvFWxHfuWqsAAKAAQACB4YVBxWoUrqMlKESKQQ")
    await message.answer("Приветствую! Выбери валюту, курс которой хочешь узнать.",
                         reply_markup=await kb.inline_values())


@router.callback_query(F.data.in_(get_currency_codes()))
async def get_currency(callback: CallbackQuery):
    # Обработчик выбора валюты, строит график курса за последний месяц и отправляет его пользователю
    try:
        currency_name = callback.data
        currency = get_actual_currency()
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        currency_data = list(filter(lambda elem: elem.code == currency_name, currency))[0]
        image_buffer = await plot_currency_rate(currency_data.code, start_date, end_date)

        await callback.answer("")
        try:
            await callback.message.delete()
        except TelegramBadRequest as e:
            logging.warning(f"Не удалось удалить сообщение: {e}")
        await callback.message.answer_photo(
            photo=BufferedInputFile(image_buffer, "graph.png"),
            caption=f"Сейчас {currency_data.name} стоит {currency_data.rate} ₽."
                    f" График стоимости {currency_data.code} "
                    f"по отношению к рублю за последний месяц",
            reply_markup=kb.back
        )
    except Exception as e:
        logging.error(f"Ошибка в обработчике get_currency: {e}")
        await callback.answer("Произошла ошибка. Попробуйте ещё раз.")


@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    # Обработчик кнопки "Назад", возвращает пользователя к выбору валюты
    await callback.answer("")
    try:
        await callback.message.delete()
    except TelegramBadRequest as e:
        logging.warning(f"Не удалось удалить сообщение: {e}")
    await callback.message.answer("Приветствую! Выбери валюту, курс которой хочешь узнать.",
                                  reply_markup=await kb.inline_values())
