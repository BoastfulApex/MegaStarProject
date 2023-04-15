from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.database import *

async def sale_keyboard():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"➕ Qo'shilish", callback_data="enter")],
            [InlineKeyboardButton(text=f"⬅️ Oldingi", callback_data="back"), InlineKeyboardButton(text=f"Keyingi ➡️", callback_data="next")],
        ]
    )
    return markup


async def sale_confirm(sale_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"✅ Qo'shilish", callback_data=f"{sale_id}")],
            [InlineKeyboardButton(text=f"⬅️ Ortga", callback_data="back")],
        ]
    )
    return markup