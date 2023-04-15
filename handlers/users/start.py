from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from utils.db_api.database import *

import re
import aiohttp
import random

async def generateOTP():
    return random.randint(111111, 999999)
import aiohttp


async def send_sms(otp, phone):
    username = 'intouch'
    password = '-u62Yq-s79HR'
    sms_data = {
        "messages":[{"recipient":f"{phone}","message-id":"abc000000003","sms":{"originator": "3700","content": {"text": f"Ваш код подтверждения для BOT: {otp}"}}}]}
    url = "http://91.204.239.44/broker-api/send"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, auth=aiohttp.BasicAuth(login=username, password=password), json=sms_data) as response:
            print(response.status)


async def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)


@dp.message_handler(commands=['start'], state='*')
async def start_func(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user is not None:
        keyboard = await menu_keyboard()
        orders_m = await get_user_monthly(message.from_id)
        orders_y = await get_user_yearly(message.from_id)
        orders_s = await get_user_seasonly(message.from_id)
        text = "👋 Mega start botiga xush kelibsiz.\n\n💰Sizda bonusgacha qoldi:\n"
        text += f"💎 Oylik : {round(orders_m, 2)}/ 10 000 000 (10 mln)\n"
        text += f"💎 Retro : {round(orders_s, 2)}/ 30 000 000 (30 mln)\n"
        text += f"💎 Yillik : {round(orders_y, 2)}/ 100 000 000 (100 mln)\n\n"
        await message.answer(text, reply_markup=keyboard)
        await state.set_state("user_menu")
    else:
        await message.answer("👋 Assalomu alaykum\nMega Star botiga xush kelibsiz Iltimos ism, sharifingizni kiriting")
        await state.set_state("get_name")


@dp.message_handler(state='get_name')
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    keyboard = await phone_keyboard()
    await message.answer("Telefon raqamininfizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇", reply_markup=keyboard)
    await state.set_state('get_phone')


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):    
    phone_number = message.contact.phone_number[1:]
    keyboard = await back_key()
    otp = await generateOTP()
    if await chek_user(phone_number):
        # await send_sms(phone=phone_number, otp=otp)
        user = await get_user_by_phone(phone_number)
        user.otp = otp
        print(otp)
        await state.update_data(phone=phone_number, action='phone')
        user.save()
        await message.answer(f"{phone_number} raqamiga yozilgan SMS ni kiriting", reply_markup=keyboard)
        await state.set_state("get_otp")
    else:
        await message.answer(f"Mijozlar ro'yxatida {phone_number} raqami bila ma'lumotlar topilmadi.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await state.set_state("non_user")
        
    
@dp.message_handler(state='get_phone', content_types=types.ContentTypes.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    phone_number = ''
    phone_number = message.text
    if not await isValid(phone_number):
        keyboard = await phone_keyboard()
        await message.answer("Telefon raqamingizni noto'g'ri formatda kiritdingiz. Iltimos, qaytadan kiriting.", reply_markup=keyboard)
        return
    otp = await generateOTP()
    if await chek_user(phone_number):
        await state.update_data(phone=phone_number)
        user = await get_user_by_phone(phone_number)
        back_keyboard = await back_key()
        user.otp = otp
        user.save()
        print(otp)
        # await send_sms(phone=phone_number, otp=otp)
        await message.answer(f"{phone_number} raqamiga yozilgan SMS ni kiriting", reply_markup=back_keyboard)
        await state.set_state("get_otp")
    else:
        await message.answer(f"Mijozlar ro'yxatida {phone_number} raqami bila ma'lumotlar topilmadi.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await state.set_state("non_user")

    
@dp.message_handler(state='get_otp', content_types=types.ContentTypes.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = await get_user_by_phone(data['phone'])
    if message.text == user.otp:
        # await set_user_telegram(phone=data['phone'], user_id=message.from_id, name=data['name'])
        keyboard = await menu_keyboard()
        print(data['name'])
        user.first_name = data['name']
        user.telegram_id = message.from_user.id
        user.save()
        orders_m = await get_user_monthly(message.from_id)
        orders_y = await get_user_yearly(message.from_id)
        orders_s = await get_user_seasonly(message.from_id)
        text = "👋 Mega star botiga xush kelibsiz.\n\n💰Sizda bonusgacha qoldi:\n"
        text += f"💎 Oylik : {round(orders_m, 2)}/ 10 000 000 (10 mln)\n"
        text += f"💎 Retro : {round(orders_s, 2)}/ 30 000 000 (30 mln)\n"
        text += f"💎 Yillik : {round(orders_y, 2)}/ 100 000 000 (100 mln)\n\n"
        await message.answer(text, reply_markup=keyboard)
        await state.set_state("user_menu")
    else:
        await message.answer("❌ Kiritiltgan tasdiqlash kodi xato. Qayta unirib ko'ring")
    
