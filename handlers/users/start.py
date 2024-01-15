from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from utils.db_api.database import *

import re
import aiohttp
import random

from aiogram.utils.deep_linking import decode_payload, get_start_link


async def generateOTP():
    return random.randint(111111, 999999)


async def send_sms(otp, phone):
    username = 'intouch'
    password = '-u62Yq-s79HR'
    sms_data = {
        "messages": [{"recipient": f"{phone}", "message-id": "abc000000003",
                      "sms": {"originator": "MEGASTAR", "content": {"text": f"Mega Star uchun tasdiqkash kodi: {otp}"}}}]}
    url = "http://91.204.239.44/broker-api/send"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, auth=aiohttp.BasicAuth(login=username, password=password),
                                json=sms_data) as response:
            print(response.status)


async def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)


@dp.message_handler(commands=['start'], state='*')
async def start_func(message: types.Message, state: FSMContext):
    args = message.get_args()
    payload = decode_payload(args)
    if payload != '':
        if check_user_is_admin(message.from_user.id):
            await message.answer("Keshbek yechildi")
        else:
            user = await get_user(message.from_user.id)
            if user is not None:
                keyboard = await menu_keyboard()
                orders_m = await get_user_monthly(message.from_id)
                orders_m_count = await get_user_monthly_count(message.from_id)
                orders_y = await get_user_yearly(message.from_id)
                orders_s = await get_user_seasonly(message.from_id)
                cashback_m = await get_cashback_monthly()
                cashback_s = await get_cashback_season()
                cashback_y = await get_cashback_year()
                text = "👋 Mega Star botiga xush kelibsiz.\n\n"
                # text += f"💎 {cashback_m.name} bonus uchun limit: {round(orders_m, 2)}/ {cashback_m.summa}\n"
                # text += f"💎 {cashback_s.name} bunus uchun limit: {round(orders_s, 2)}/ {cashback_s.summa}\n"
                # text += f"💎 {cashback_y.name} bunus uchun limit: {round(orders_y, 2)}/ {cashback_y.summa}\n\n"
                text += f"💎 2% 2-6 mln so'm    {round(orders_m, 2)}/ 6000000.00 so'm\n"
                text += f"💎 3% 6-12 mln so'm    {round(orders_m, 2)}/ 12000000.00 so'm\n"
                text += f"💎 5% 12 mln + so'm    {round(orders_m, 2)}/ 12000000.00 so'm\n"
                text += f"\n💎 3% 500-1000     {round(orders_m_count, 2)}/ 500 ta\n"
                text += f"💎 5% 1000 +     {round(orders_m_count, 2)}/ 1000 ta\n"
                text += f"💎\n 5% 25 mln + so'm    {round(orders_m, 2)}/ 25000000.00 so'm\n"
                await message.answer(text, reply_markup=keyboard)
                await state.set_state("user_menu")
            else:
                await message.answer(
                    "👋 Assalomu alaykum\nMega Star botiga xush kelibsiz Iltimos ism, sharifingizni kiriting")
                await state.set_state("get_name")
    else:
        user = await get_user(message.from_user.id)
        if user is not None:
            keyboard = await menu_keyboard()
            orders_m = await get_user_monthly(message.from_id)
            orders_y = await get_user_yearly(message.from_id)
            orders_s = await get_user_seasonly(message.from_id)
            cashback_m = await get_cashback_monthly()
            cashback_s = await get_cashback_season()
            cashback_y = await get_cashback_year()
            text = "👋 Mega Star botiga xush kelibsiz.\n\n"
            text += f"💎 {cashback_m.name} bonus uchun limit: {round(orders_m, 2)}/ {cashback_m.summa}\n"
            text += f"💎 {cashback_s.name} bunus uchun limit: {round(orders_s, 2)}/ {cashback_s.summa}\n"
            text += f"💎 {cashback_y.name} bunus uchun limit: {round(orders_y, 2)}/ {cashback_y.summa}\n\n"
            await message.answer(text, reply_markup=keyboard)
            await state.set_state("user_menu")
        else:
            await message.answer("👋 Assalomu alaykum\nMega Star botiga xush kelibsiz Iltimos ism,"
                                 " sharifingizni kiriting")
            await state.set_state("get_name")


@dp.message_handler(state='get_name')
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    keyboard = await phone_keyboard()
    await message.answer("Telefon raqamininfizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇",
                         reply_markup=keyboard)
    await state.set_state('get_phone')


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    print(message.contact.phone_number)
    phone_number = message.contact.phone_number.split('+')[0]
    keyboard = await back_key()
    if await chek_user(phone_number):
        otp = await generateOTP()
        user = await get_user_by_phone(phone_number)
        await state.update_data(phone=phone_number, action='phone')
        user.otp = otp
        print(otp)
        user.save()
        await send_sms(phone=phone_number, otp=user.otp)
        await message.answer(f"+{phone_number} raqamiga yozilgan 📩 SMS ni kiriting 👇", reply_markup=keyboard)
        await state.set_state("get_otp")
    else:
        keyboard = await phone_keyboard()
        await message.answer(f"🚫 Mijozlar ro'yxatida +{phone_number} raqami bilan ma'lumotlar topilmadi.",
                             reply_markup=keyboard)


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not await isValid(phone_number):
        keyboard = await phone_keyboard()
        await message.answer("⚠️ Telefon raqamingizni noto'g'ri kiritdingiz. Iltimos, qaytadan kiriting.",
                             reply_markup=keyboard)
        return
    elif await chek_user(phone_number):
        await state.update_data(phone=phone_number)
        user = await get_user_by_phone(phone_number)
        otp = await generateOTP()
        back_keyboard = await back_key()
        user.otp = otp
        print(otp)
        user.save()
        await send_sms(phone=phone_number, otp=user.otp)
        await message.answer(f"+{phone_number} raqamiga yozilgan 📩 SMS ni kiriting 👇", reply_markup=back_keyboard)
        await state.set_state("get_otp")
    else:
        keyboard = await phone_keyboard()
        await message.answer(f"🚫 Mijozlar ro'yxatida +{phone_number} raqami bila ma'lumotlar topilmadi.",
                             reply_markup=keyboard)


@dp.message_handler(state='get_otp', content_types=types.ContentTypes.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = await get_user_by_phone(data['phone'])
    if message.text == user.otp:
        user.first_name = data['name']
        user.telegram_id = message.from_user.id
        user.save()
        keyboard = await menu_keyboard()
        orders_m = await get_user_monthly(message.from_id)
        orders_y = await get_user_yearly(message.from_id)
        orders_s = await get_user_seasonly(message.from_id)
        cashback_m = await get_cashback_monthly()
        cashback_s = await get_cashback_season()
        cashback_y = await get_cashback_year()
        text = "👋 Mega Star botiga xush kelibsiz.\n\n"
        text += f"💎 {cashback_m.name} bonus uchun limit: {round(orders_m, 2)}/ {cashback_m.summa}\n"
        text += f"💎 {cashback_s.name} bunus uchun limit: {round(orders_s, 2)}/ {cashback_s.summa}\n"
        text += f"💎 {cashback_y.name} bunus uchun limit: {round(orders_y, 2)}/ {cashback_y.summa}\n\n"
        await message.answer(text, reply_markup=keyboard)
        await state.set_state("user_menu")
    else:
        await message.answer("❌ Kiritiltgan tasdiqlash kodi xato. Qayta unirib ko'ring")
