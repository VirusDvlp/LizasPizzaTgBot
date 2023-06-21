import re

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text


from texts import start, registration_1, registration_2, registration_3
from FSM import RegisterStates, UserSettingsFSM
from create_bot import db
from Keyboards import get_main_kb, get_user_settings_kb
from other import check_email_address


async def cmd_start(message: types.Message) -> None: 
    if db.check_user_exists(message.from_user.id): #Check if user in the DB
        await message.answer(text=start, reply_markup=get_main_kb(message.from_user.id))
    else:
        await message.answer(text=registration_1)
        await RegisterStates.email_state.set()


async def register_email(message: types.Message, state: FSMContext) -> None: #Catch email
    email = message.text
    if check_email_address(email):
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            data['chat_id'] = message.chat.id
            data['email'] = email
        await message.answer(text=registration_2)
        await RegisterStates.date_state.set()
    else:
        await message.answer(text='Почта\tвведена\tневерно')


async def register_date(message: types.Message, state: FSMContext) -> None: # Catch birthday of user
    if re.findall(r"((?:[1-3][0-9]|[0][1-9])(?:[0][1-9]|[1][0-2])[1-2][0-9]\d\d)", message.text): # Date must be like ddMMyyyy
        async with state.proxy() as data:
            data['date'] = int(message.text)
            await message.answer(registration_3)
            await RegisterStates.location_state.set()
    else:
        await message.answer('Дата\tвведена\tневерно')


async def register_location(message: types.Message, state: FSMContext) -> None: # Catch default location and finish FSM
    async with state.proxy() as data:
        db.add_user(data['user_id'], data['email'], 
        float(message.location.latitude), float(message.location.longitude), data['date'])
        db.close_db()
    await message.location.bot.send_message(chat_id=data['chat_id'], text='Прекрасно, регистрация прошла успешно!', reply_markup=get_main_kb(message.from_user.id))
    await state.finish()


async def edit_user_settings(message: types.Message) -> None:
    await message.answer('Выберите,\tчто\tхотите\tизменить', reply_markup=get_user_settings_kb())
    await UserSettingsFSM.what_state.set()


async def edit_email(callback: types.CallbackQuery):
    await callback.message.answer('Пришлите\tадрес\tэлектронной\tпочты')
    await UserSettingsFSM.email_state.set()
    await callback.answer()


async def check_email(message: types.Message, state: FSMContext) -> None:
    if check_email_address(message.text):
        db.edit_user_email(message.text, message.from_user.id)
        await message.answer('Почта\tуспешно\tизменена', reply_markup=get_main_kb(message.from_user.id))
        await state.finish()
    else:
        await message.answer('Почта\tуказана\tневерно,\tпопробуйте\tеще\tраз')
    

async def edit_address(callback: types.CallbackQuery) -> None:
    await callback.message.answer('Пришлите\tсвою\tосновную\tгеолокацию')
    await UserSettingsFSM.location_state.set()
    await callback.answer()


async def get_location(message: types.Message, state: FSMContext) -> None:
    db.edit_user_address(
        message.from_user.id,
        message.location.latitude,
        message.location.longitude
    )
    await message.answer('Адресс\tдоставки\tупешно\tизменен')
    await state.finish()


async def get_wrong_location(message: types.Message) -> None:

    '''if user sent not geolocation'''

    await message.answer('Геолокация\tуказана\tневерно,\tпопробуте\tеще\tраз')


def register_handlers_reg(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(register_email, state=RegisterStates.email_state)
    dp.register_message_handler(register_date, state=RegisterStates.date_state)
    dp.register_message_handler(register_location, state=RegisterStates.location_state, content_types=['location'])
    dp.register_message_handler(edit_user_settings, Text('ИЗМЕНИТЬ ПАРАМЕТРЫ ПРОФИЛЯ⚙️'))
    dp.register_callback_query_handler(edit_email, Text('email'), state=UserSettingsFSM.what_state)
    dp.register_callback_query_handler(edit_address, Text('address'), state=UserSettingsFSM.what_state)
    dp.register_message_handler(check_email, state=UserSettingsFSM.email_state)
    dp.register_message_handler(get_location, content_types=['location'], state=UserSettingsFSM.location_state)
    dp.register_message_handler(get_wrong_location, state=UserSettingsFSM.location_state)
