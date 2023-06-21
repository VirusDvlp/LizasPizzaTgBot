from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from Keyboards import get_basket_kb, get_finish_order_kb
from create_bot import db
from FSM import BasketFSM
from aiogram.dispatcher.storage import FSMContext
from .menu_handlers import send_menu


async def show_basket(message: types.Message, state: FSMContext) -> None:
    await BasketFSM.edit_basket_state.set()
    async with state.proxy() as data:
        data['page'] = 0 # page of basket
    await message.answer('👍', reply_markup=get_finish_order_kb())
    await message.answer(text='Корзина', reply_markup=get_basket_kb(message.from_user.id, 0))


async def add_pizza(callback: types.CallbackQuery, state: FSMContext) -> None:
    pizza = callback.data.split('_')[1] # bot get pizza like add_<pizza_id>_<pizza_size>
    db.add_to_basket(user_id=callback.from_user.id, pizza=pizza)
    db.close_db()
    async with state.proxy() as data:
        await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
        message_id=callback.message.message_id, reply_markup=get_basket_kb(callback.from_user.id, data['page']))


async def del_pizza(callback: types.CallbackQuery, state: FSMContext) -> None:
    pizza = callback.data.split('_')[1] # bot get pizza like del_<pizza_id>_<pizza_size>
    db.delete_from_basket(pizza, callback.from_user.id)
    db.close_db()
    async with state.proxy() as data:
        await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
        message_id=callback.message.message_id, reply_markup=get_basket_kb(callback.from_user.id, data['page']))


async def kill_pizza(callback: types.CallbackQuery, state: FSMContext) -> None:
    pizza = callback.data.split('_')[1] # bot get pizza like kill_<pizza_id>_<pizza_size>
    db.kill_pizza_basket(pizza, callback.from_user.id)
    db.close_db()
    async with state.proxy() as data:
            await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
            message_id=callback.message.message_id, reply_markup=get_basket_kb(callback.from_user.id, data['page']))


async def prev_page(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['page'] -= 1
        await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
        message_id=callback.message.message_id, reply_markup=get_basket_kb(callback.from_user.id, data['page']))
        await callback.answer(f"Страница_{data['page'] + 1}")


async def next_page(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['page'] += 1
        await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
        message_id=callback.message.message_id, reply_markup=get_basket_kb(callback.from_user.id, data['page']))
        await callback.answer(f"Страница_{data['page'] + 1}")

async def go_to_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.finish()
    await send_menu(callback.message)
    await callback.answer('Открыто\tменю')

async def answ_other_callback(callback: types.CallbackQuery):
    await callback.answer(callback.data[1 : -1])


def register_basket_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(show_basket, Text('СДЕЛАТЬ ЗАКАЗ🛒'))
    dp.register_callback_query_handler(add_pizza, Text(startswith='add_'), state=BasketFSM.edit_basket_state)
    dp.register_callback_query_handler(del_pizza, Text(startswith='del_'), state=BasketFSM.edit_basket_state)
    dp.register_callback_query_handler(kill_pizza, Text(startswith='kill_'), state=BasketFSM.edit_basket_state)
    dp.register_callback_query_handler(prev_page, Text('prev'), state=BasketFSM.edit_basket_state)
    dp.register_callback_query_handler(next_page, Text('next'), state=BasketFSM.edit_basket_state)
    dp.register_callback_query_handler(go_to_menu, Text('menu'), state=BasketFSM.edit_basket_state)
    dp.register_callback_query_handler(answ_other_callback, Text(startswith='o'), state=BasketFSM.edit_basket_state)
