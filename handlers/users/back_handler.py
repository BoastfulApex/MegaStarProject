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


@dp.message_handler(commands=["start"])
async def handler(message: types.Message):
    args = message.get_args()
    payload = decode_payload(args)
    if payload != '':
        print(payload)
        kod = await get_ishlatilgan(payload)
        if kod is None:
            print(kod)
            pay = await get_kesh(payload)
            markup = await get_my_money()
            await message.answer(f"Xisobingizga {pay.summa} keshbek qabul qilindi", reply_markup=markup)
            await add_ishlatilgan(user_id=message.from_user.id, kod=payload, summa=pay.summa)
            pul = pay.summa
            print(pul)
            await add_pay(user_id=message.from_user.id, summa=pul, name=message.from_user.full_name)
        else:
            markup = await get_my_money()
            await message.answer('Bu kod oldin ishlatilgan', reply_markup=markup)
    else:
        await message.answer(f'Iltimos botdan qr kod orqali foydalaning 📲')