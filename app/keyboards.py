"""
В этом файле выполняются такие задачи:

1. Создание инлайн-клавиатуры с кнопкой "Назад" для возврата к выбору валюты.

Функция inline_values():
2. Создание инлайн-клавиатуры с кнопками для выбора валюты, используя актуальные данные о валютах.
3. Форматирование кнопок с отображением кода и названия валюты.
4. Возвращение клавиатуры в виде объекта, готового к использованию в Telegram.
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.currency_rate import get_actual_currency

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])


async def inline_values():
    # Создает инлайн-клавиатуру с кнопками для выбора валюты
    keyboard = InlineKeyboardBuilder()
    currencies = get_actual_currency()

    for currency in currencies:
        name = currency.name
        code = currency.code
        keyboard.add(InlineKeyboardButton(text=f"{code} ({name})", callback_data=code))
    return keyboard.adjust(2).as_markup()
