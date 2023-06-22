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


@dp.message_handler(lambda message: message.text == '⬅️ Orqaga', state='get_otp')
async def back_funcktion(message: types.Message, state: FSMContext):
    keyboard = await phone_keyboard()
    await message.answer(text="Telefon raqamininfizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇", reply_markup=keyboard)
    await state.set_state("get_phone")


@dp.message_handler(lambda message: message.text == '⬅️ Orqaga', state='get_comment')
async def back_funcktion(message: types.Message, state: FSMContext):
    keyboard = await menu_keyboard()
    await message.answer(text="Kerakli bo'limni tanlang 👇", reply_markup=keyboard)
    await state.set_state("user_menu")


@dp.message_handler(lambda message: message.text == '⬅️ Orqaga', state='aksiya')
async def back_funcktion(message: types.Message, state: FSMContext):
    keyboard = await menu_keyboard()
    await message.answer(text="Kerakli bo'limni tanlang 👇", reply_markup=keyboard)
    await state.set_state("user_menu")
