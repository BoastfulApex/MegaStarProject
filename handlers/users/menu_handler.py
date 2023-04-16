from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *
import qrcode

@dp.message_handler(state='user_menu')
async def menu(message: types.Message, state: FSMContext):
    await state.update_data(action='menu')
    if message.text == "Mening hisobim/Bonuslarim":
        keyboard = await menu_keyboard()
        orders_m = await get_user_monthly(message.from_id)
        orders_y = await get_user_yearly(message.from_id)
        orders_s = await get_user_seasonly(message.from_id)
        cashbacks = await get_user_kashbacks(message.from_user.id)
        user_sales = await get_user_sales(message.from_id)
        text = f"💵Ushbu oydagi xaridlar: {round(orders_m, 2)}\n"
        text += f"\n💰Sizda bonusgacha qoldi:\n    💵 Oylik: {round(orders_m, 2)}/10 000 000 (10 mln)\n    💵 Retro: {round(orders_s, 2)}/30 000 000 (30mln)\n"
        text += f"    💵 Yillik : {round(orders_y, 2)}/100 000 000 (100 mln)\n"
        text += f"\nQo'shimcha aksiyalar: \n"
        for sale in user_sales:
            text += f"📌{sale.sale.name}\n   {sale.sale.required_quantity} dona {sale.sale.product.itemname} uchun {sale.sale.gift_quantity} dona {sale.sale.gift_product.itemname}\n    {sale.order_quantity}/{sale.sale.required_quantity}. Muddat: {sale.sale.expiration_date.strftime('%d.%m.%Y')}"
        text += f"\n\nHozirgi keshbek: {cashbacks}"
        await message.answer(text, reply_markup=keyboard)
    if message.text == "Joriy aksiyalar":
        await state.update_data(sale_id=0)
        back_keyboard = await back_key()
        await message.answer("Hozirda aktiv bo'lgan aksiyalar 👇", reply_markup=back_keyboard)
        sale = await get_active_sales()
        try:
            sale = sale[0]
            text = f"🔥 {sale.name}\n\n 🎁{sale.required_quantity} dona {sale.product.itemname} uchun {sale.gift_quantity} dona {sale.gift_product.itemname}\n Aksiya amal qilish muddati {sale.expiration_date.strftime('%d.%m.%Y')} gacha"
            keyboard = await sale_keyboard() 
            await message.answer(text, reply_markup=keyboard)
        except:
            pass
        await state.set_state('aksiya')
    if message.text == "Izoh qoldirish":
        keyboard = await back_key()
        await message.answer("ltimos o'z izohingizni shu yerda yozib qoldiring 👇\n"
                             "Mutaxassislarimiz o'rganib chiqib tez orada sizga "
                             "javob berishadi", 
                             reply_markup=keyboard)
        await state.set_state("get_comment")
    if message.text == 'QrCode':
        user = await get_user(message.from_id)
        q = qrcode.make(f'{user.id}')
        q.save('qrcode.png')
        keyboard = await menu_keyboard()
        photo = open('qrcode.png', 'rb')
        cashbacks = await get_user_kashbacks(message.from_user.id)  
        await message.answer_photo(photo=photo, caption=f"Sizning keshbekingizni ishlatish uchun QR codingiz 👆\n\nHozirgi keshbekingiz: {cashbacks} UZS", reply_markup=keyboard)
    if message.text == "To'lovlar tarixi":
        orders = await get_orders(message.from_id)
        text = "To'lovlaringiz tarixi:\n\n"
        i = 1
        for order in orders:
            details = await get_order_details(order.id)
            text = f"{i})🗓 Sana: {order.created_date.strftime('%d.%m.%Y')},  Summa: {round(order.summa, 2)}\n"
            for detail in details:
                text += f"   {detail.product.itemname} ✖️ {detail.count}  {detail.total_uzs}\n"
            chunks = [text[i:i+4096] for i in range(0, len(text), 4096)] # split the text into chunks of 4096 characters
            for chunk in chunks:
                await message.answer(chunk)
            i += 1    
        if message.text == "Yangiliklar":
            await message.answer("Yangiliklar")


@dp.message_handler(state="get_comment")
async def get_comment(message: types.Message, state: FSMContext):
    await add_comment(user_id=message.from_user.id, comment=message.text)
    keyboard = await menu_keyboard()
    await message.answer("Murojaatingiz o'rganish uchun mutaxassisimizga yetkazildi\n"
                         "Kerakli bo'limni tanlang", reply_markup=keyboard)
    await state.set_state("user_menu")

    
@dp.callback_query_handler(state="aksiya")
async def aksiya_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    indexation = int(data['sale_id'])
    sale = await get_active_sales()
    if call.data == "enter":
        sale = sale[indexation]
        keyboard = await sale_confirm(sale.id)
        text = f"{sale.name} \nAksiyasiga qo'shilishni istaysizmi"
        await call.message.edit_text(text, reply_markup=keyboard)
        await state.set_state('sale_enter')
        return
    elif call.data == "next":
        indexation = (indexation + 1) % len(sale)
    elif call.data == "back":
        indexation = (indexation - 1) % len(sale)
    sale = sale[indexation]
    text = f"🔥 {sale.name}\n\n 🎁 {sale.required_quantity} dona {sale.product.itemname} uchun {sale.gift_quantity} dona {sale.gift_product.itemname}\n Aksiya amal qilish muddati {sale.expiration_date.strftime('%d.%m.%Y')} gacha"
    keyboard = await sale_keyboard()
    await state.update_data(sale_id=indexation)
    await call.message.edit_text(text, reply_markup=keyboard)
    await state.set_state('aksiya')
    

@dp.callback_query_handler(state='sale_enter')
async def sale_enter(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data == 'back':
        indexation = int(data['sale_id'])
        sale = await get_active_sales()
        sale = sale[indexation]
        text = f"🔥 {sale.name}\n\n 🎁 {sale.required_quantity} dona {sale.product.itemname} uchun {sale.gift_quantity} dona {sale.gift_product.itemname}\n Aksiya amal qilish muddati {sale.expiration_date.strftime('%d.%m.%Y')} gacha"
        keyboard = await sale_keyboard()
        await call.message.edit_text(text, reply_markup=keyboard)
        await state.set_state('aksiya')
    else:
        sale = await get_sale(call.data)
        user_s = await add_user_sale(user_id=call.from_user.id, sale_id=call.data)
        await call.message.delete()
        keyboard = await menu_keyboard()
        text = f"💥 Siz <b>{sale.name}</b> aksiyasi ishtirokchisiga aylandingiz.\n🗓 Aksiya muddati {sale.expiration_date.strftime('%d.%m.%Y')}\n\nKerakli bo'limni tanlang"
        await bot.send_message(text=text, chat_id=call.from_user.id, reply_markup=keyboard)
        await state.set_state('user_menu')