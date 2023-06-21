from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from FSM import BasketFSM
from create_bot import db
from Keyboards import get_order_type_kb, get_spec_adress_kb, get_shop_adress_kb, get_payment_type_kb, get_online_payments_kb, get_main_kb
from texts import get_invoice_descr, get_final_order_message_1, get_final_order_message_2, get_order_message
from config import PAYMENT_TOKENS, SHOP_ADDRESSES, ADMIN_ID
from other import get_basket


async def order_type(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['total'] = int(callback.data.split('_')[1]) # We get callback data as order_<total>
        data['home_address'] = (0, 0) # delivering address
        data['shop_address'] = 0
    await callback.message.answer(text='Выберите,\tкак\tвы\tхотите\tполучить\tзаказ', reply_markup=get_order_type_kb())
    await BasketFSM.adress_state.set()
    await callback.answer('Оформление\tзаказа')


async def specify_home_adress(callback: types.CallbackQuery, state: FSMContext) -> None:

    '''bot ask user address of delivering: default or another?'''

    async with state.proxy() as data:
        data['type'] = callback.data
        data['home_address'] = db.get_user_address(callback.from_user.id)
        await callback.message.answer_location(data['home_address'][0], data['home_address'][1])
        await callback.message.answer('Вы хотите полуить доставку по этому адресу?', reply_markup=get_spec_adress_kb())
    await BasketFSM.home_adress_state.set()
    await callback.answer()


async def default_home_adress(callback: types.CallbackQuery) -> None:
    await BasketFSM.payment_type_state.set()
    await callback.message.answer('Выберите тип оплаты', reply_markup=get_payment_type_kb(1))
    await callback.answer()



async def ask_another_adress(callback: types.CallbackQuery) -> None:
    await BasketFSM.get_home_adress_state.set()
    await callback.message.answer('Пришлите геолокацию, соответсвующую месту доставки')


async def get_home_adress(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['home_address'] = (message.location.latitude, message.location.longitude)
    await BasketFSM.payment_type_state.set()
    await message.answer(text='Выберите тип оплаты', reply_markup=get_payment_type_kb(1))


async def get_wrong_home_adress(message: types.Message) -> None:

    '''if user sent not geolocation'''

    await message.answer('Неверно указан адрес. Отправьте ещё раз.')


async def shop_adress(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['type'] = callback.data
    await BasketFSM.get_shop_adress_state.set()
    await callback.message.answer('Выберите адресс магазина', reply_markup=get_shop_adress_kb())
    await callback.answer()


async def get_shop_adress(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['shop_address'] = SHOP_ADDRESSES[callback.data]
    await BasketFSM.payment_type_state.set()
    await callback.message.answer('Выберите тип оплаты', reply_markup=get_payment_type_kb(2))
    await callback.answer()


async def offline_payment(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        await callback.message.answer(get_final_order_message_1(callback.data, data['total'], data['shop_address']), reply_markup=get_main_kb(callback.from_user.id))
        user_id = callback.from_user.id
        db.make_order(
            callback.from_user.id,
            str(callback.message.date.date()) + str(callback.message.date.time()),
            data['home_address'][0],
            data['home_address'][1],
            data['total'],
            data['shop_address'],
            int(data['type'])       
        )

        await callback.message.bot.send_message( # bot send to admin notification about order
            ADMIN_ID,
            get_order_message(
                get_basket(db.get_basket(user_id)),
                data['total'],
                data['type'],
                '2',
                db.get_order_id(),
                db.get_user_email(user_id),
                data['shop_address'],
                data['home_address']
            )
        )
        if data['home_address'] != (0, 0): 
            await callback.message.bot.send_location(  # if order must be delivered bot send to admin delivering address
                ADMIN_ID,
                data['home_address'][0],
                data['home_address'][1]
            )
    await state.finish()
    await callback.answer()


async def online_payment(callback: types.CallbackQuery) -> None:
    await callback.message.answer(
        'Выберите платёжную систему, через которую хотите провести оплату:',
        reply_markup=get_online_payments_kb()
    )
    await BasketFSM.invoice_state.set()
    await callback.answer()


async def send_amount(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        lb_invoice = types.LabeledPrice('Заказ', data['total'] * 100)
        await callback.bot.send_invoice(
            chat_id=callback.message.chat.id,
            title='Оплата заказа ',
            description=get_invoice_descr(data['home_address'], data['total']),
            payload='test-invoice-payload',
            provider_token=PAYMENT_TOKENS[callback.data],
            currency='rub',
            prices=[lb_invoice]
        )
    await callback.answer()


async def pre_check_out_query(pre_check_out: types.PreCheckoutQuery)  -> None:
    await pre_check_out.bot.answer_pre_checkout_query(pre_check_out.id, ok=True)


async def succesfull_payment(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    async with state.proxy() as data:
        db.make_order(
            user_id,
            message.date.date + message.date.time,
            data['home_address'][0],
            data['home_address'][1],
            data['total'],
            data['shop_address'],
            int(data['type'])
        )
        await message.answer(get_final_order_message_2(data['shop_address'], data['type']), reply_markup=get_main_kb(message.from_user.id))
        
        await message.bot.send_message( # bot send to admin notification about order
            ADMIN_ID,
            get_order_message(
                get_basket(db.get_basket(user_id)),
                data['total'],
                data['type'],
                '1',
                db.get_order_id(),
                db.get_user_email(user_id),
                data['shop_address'],
                data['home_address']
            )
        )
        if data['home_address'] != (0, 0): # if order must be delivered bot send to admin delivering address
            await message.bot.send_location(
                ADMIN_ID,
                data['home_address'][0],
                data['home_address'][1]
            )
        db.clear_basket(user_id)
    await state.finish()


async def finish_order(message: types.Message, state: FSMContext) -> None:
    await message.answer('Офорление заказа отменено', reply_markup=get_main_kb(message.from_user.id))
    await state.finish()


def register_order_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(order_type, Text(startswith='order'), state=BasketFSM.edit_basket_state)
    dp.register_callback_query_handler(specify_home_adress, Text('1'), state=BasketFSM.adress_state)
    dp.register_callback_query_handler(default_home_adress, Text('1'), state=BasketFSM.home_adress_state)
    dp.register_callback_query_handler(ask_another_adress, Text('2'), state=BasketFSM.home_adress_state)
    dp.register_callback_query_handler(default_home_adress, Text('1'), state=BasketFSM.home_adress_state)
    dp.register_message_handler(get_home_adress, content_types=['location'],state=BasketFSM.get_home_adress_state)
    dp.register_message_handler(get_wrong_home_adress, state=BasketFSM.get_home_adress_state)
    dp.register_callback_query_handler(shop_adress, Text('2'), state=BasketFSM.adress_state)
    dp.register_callback_query_handler(get_shop_adress, state=BasketFSM.get_shop_adress_state)
    dp.register_callback_query_handler(online_payment, Text('1'), state=BasketFSM.payment_type_state)
    dp.register_callback_query_handler(send_amount, state=BasketFSM.invoice_state)
    dp.register_pre_checkout_query_handler(pre_check_out_query, state=BasketFSM.invoice_state)
    dp.register_message_handler(succesfull_payment, content_types=types.ContentType.SUCCESSFUL_PAYMENT)
    dp.register_callback_query_handler(offline_payment, state=BasketFSM.payment_type_state)
    dp.register_message_handler(finish_order, Text('ВЫЙТИ ИЗ КОРЗИНЫ🔙'), state=BasketFSM.all_states)
