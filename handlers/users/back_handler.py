from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from utils.db_api.database import *

BackCongfig = {
    'phone': {
        "state": "get_phone",
        "text": "Telefon raqamininfizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇",
        "keyboard": phone_keyboard(),
    },
    'menu': {
        "state": "user_menu",
        "text": "Kerakli bo'limni tanlang",
        "keyboard": menu_keyboard(),
    }
}


@dp.message_handler(lambda message: message.text == '⬅️ Orqaga', state='*')
async def back_funcktion(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data['action']
    keybpard = await BackCongfig[action]['keyboard']
    await message.answer(text=BackCongfig[action]['text'], reply_markup=keybpard)
    await state.set_state(BackCongfig[action]['state'])
