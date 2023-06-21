from aiogram import types, Dispatcher
from create_bot import db
from Keyboards import get_pizza_kb, get_size_kb, get_main_kb
from texts import get_pizza_text
from aiogram.dispatcher.filters import Text
from FSM import MenuFSM
from aiogram.dispatcher.storage import FSMContext


async def send_menu(message: types.Message) -> None:

    '''Send every pizzas with themsselves name, descr, keyboard and if for callback'''

    await message.answer('Меню', reply_markup=get_main_kb(message.from_user.id))
    pizzas = db.get_menu()
    [await message.answer_photo(        
        photo=pizza[2],
        caption=get_pizza_text(pizza[0], pizza[3], pizza[1]),
        reply_markup=get_pizza_kb(str(pizza[4])),
        parse_mode=types.ParseMode.HTML
    )for pizza in pizzas]


async def choice_pizza_size(callback: types.CallbackQuery, state: FSMContext) -> None:
    '''Ask to choice size with Inline keyboard'''
    async with state.proxy() as data:
        data['pizza_id'] = callback.data
    await callback.bot.edit_message_reply_markup(message_id=callback.message.message_id,
    chat_id=callback.message.chat.id, reply_markup=get_size_kb()) # Change keyboard under the pizza image
    await MenuFSM.size_state.set()
    await callback.answer(text='Выберите\tразмер\tпиццы')


async def add_to_basket(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['size'] = callback.data
        db.add_to_basket(f"{data['pizza_id']}*{data['size']}", callback.from_user.id)
        db.close_db()
        await callback.bot.edit_message_reply_markup(message_id=callback.message.message_id,
        chat_id=callback.message.chat.id, reply_markup=get_pizza_kb(data['pizza_id']))
    await state.finish()
    await callback.answer(text='Пицца\tуспешно\tдобавлена\tв\tкорзину')


def register_menu_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(send_menu, Text('МЕНЮ📋'))
    dp.register_callback_query_handler(choice_pizza_size)
    dp.register_callback_query_handler(add_to_basket, state=MenuFSM.size_state)

