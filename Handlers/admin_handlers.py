from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter, Text

from create_bot import db
from FSM import NewPizzaFSM, RedactPizzaFSM, MailingFSM, MainAdminFSM
from config import ADMIN_ID
from Keyboards import get_choice_change_kb, get_pizza_list_kb, get_what_change_kb, get_main_kb, get_cancel_kb, get_add_bt_kb
from texts import redact_pizza_text


async def admin_mode(message: types.Message) -> None:
    await message.answer('Открыта\tпанель\tадминистратора', reply_markup=get_choice_change_kb())
    await MainAdminFSM.admin_state.set()


async def exit_admin_mode(message: types.Message, state: FSMContext) -> None:
    await message.answer('Панель\tадминистратора\tзакрыта', reply_markup=get_main_kb(message.from_user.id))
    await state.finish()


async def exit_change_mode(message: types.Message, state: FSMContext) -> None:
    await MainAdminFSM.admin_state.set()
    await message.answer('👍', reply_markup=get_choice_change_kb())


async def new_pizza(message: types.Message):
    await message.answer('Выберите\tназвание\tдля\tпиццы', reply_markup=get_cancel_kb('СОЗДАНИЕ\tПИЦЦЫ'))
    await NewPizzaFSM.name_state.set()


async def get_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Хорошее\tназвание👍Теперь\tопределите\tцену\tпиццы')
    await NewPizzaFSM.price_state.set()


async def get_price(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Принято.\tСейчас\tнадо\tпридумать\tописание')
    await NewPizzaFSM.descr_state.set()


async def get_descr(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['descr'] = message.text
    await message.answer('Отлично.\tТеперь\tпришлите\t<b>ссылку</b>\tна\tфотографию\tданной\tпиццы', parse_mode=types.ParseMode.HTML)
    await NewPizzaFSM.image_state.set()


async def insert_pizza(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        db.add_pizza_in_db(
            data['name'],
            data['descr'],
            data['price'],
            message.text
        )
    await message.answer('Пицца\tуспешно\tдобавлена\tв\tменю', reply_markup=get_choice_change_kb())
    await MainAdminFSM.admin_state.set()


async def redact_pizza(message: types.Message) -> None:
    await message.answer('Редактирование\tпиццы', reply_markup=get_cancel_kb('РЕДАКТИРОВАНИЕ\tПИЦЦЫ'))
    await message.answer('Выберите,\tкакую\tпиццу\tхотите\tредактировать', reply_markup=get_pizza_list_kb())
    await RedactPizzaFSM.pizza_state.set()


async def get_pizza(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['pizza_id'] = callback.data
    await callback.message.answer('Теперь\tвыберите,\tчто\tвы\tхотите\tредактировать', reply_markup=get_what_change_kb())
    await RedactPizzaFSM.what_state.set()
    await callback.answer()


async def get_what_change(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['what_change'] = callback.data
        await callback.message.answer(redact_pizza_text[callback.data], types.ParseMode.HTML)
        await RedactPizzaFSM.change_state.set()
        await callback.answer()


async def get_change(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        db.redact_pizza(data['pizza_id'], data['what_change'], message.text)
    await message.answer('Параметры\tпиццы\tуспешно\tизменены', reply_markup=get_choice_change_kb())
    await MainAdminFSM.admin_state.set()


async def make_mailing(message: types.Message) -> None:
    await message.answer('Пришлите\tфотографии\tк\tвашей\tрассылке', reply_markup=get_cancel_kb('РАССЫЛКУ'))
    await MailingFSM.photo_state.set()


async def get_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.answer('Теперь\tпришлите\tтекст\tсообщения\tв\tвашей\tрассылке')
    await MailingFSM.text_state.set()


async def get_text(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['text'] = message.text
        data['keyboard'] = types.InlineKeyboardMarkup(1)
        await message.answer_photo(
            data['photo'],
            'СЕЙЧАС\tВАШЕ\tСООБЩЕНИЕ\tВЫГЛЯДЕТ\tТАК:\n' + message.text,
            reply_markup=data['keyboard']
        )
    await message.answer('''Теперь\tопределите\tбудут\tли\tв\tвашем\tсообщении\tкнопки\n
    Если\tда,\tто\tнажмите\t"ДОБАВИТЬ КНОПКУ",\tа\tесли\tнет,\tто\tкнопку\tниже
    (Учтите,\tчто\tпосле\tэтого\tсобщение\tразошлется\tвсем\tпользователям)''',
    reply_markup=get_add_bt_kb())
    await MailingFSM.add_button_state.set()
    

async def add_bt(callback: types.CallbackQuery) -> None:
    await callback.message.answer('Пришлите\tтекст\tвашей\tкнопки')
    await MailingFSM.button_text_state.set()
    await callback.answer()


async def get_bt_text(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['bt_text'] = message.text
    await message.answer('Теперь\tпришлите\tссылку,\tна\tкоторую\tбудет\tввести\tкнопка')
    await MailingFSM.button_url_state.set()


async def get_bt_url(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['keyboard'].add(types.InlineKeyboardButton(data['bt_text'], message.text))
        await message.answer_photo(
            data['photo'],
            'СЕЙЧАС\tВАШЕ\tСООБЩЕНИЕ\tВЫГЛЯДЕТ\tТАК:\n' + data['text'],
            reply_markup=data['keyboard']
        )
    await MailingFSM.add_button_state.set()
    await message.answer('Кнопка\tуспешно\tдобавлена', reply_markup=get_add_bt_kb())


async def send_mailing(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        keyboard = data['keyboard']
        users = db.get_user_id_list()
        for user in users:
            try:
                await callback.bot.send_photo(
                    user[0],
                    photo=data['photo'],
                    caption=data['text'],
                    reply_markup=keyboard
                )
            except Exception:
                continue
    await state.finish()
    await callback.message.answer('Рассылка\tуспешно\tсоздана', reply_markup=get_choice_change_kb())
    await MainAdminFSM.admin_state.set()
    await callback.answer()
        

def register_admin_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(admin_mode, Text('АДМИН-ПАНЕЛЬ💻'), IDFilter(ADMIN_ID))
    dp.register_message_handler(exit_admin_mode, Text('ВЫЙТИ ИЗ РЕЖИМА АДМИНИСТРТАТОРА🔙'), state=MainAdminFSM.admin_state)
    dp.register_message_handler(
        exit_change_mode,
        Text(startswith='ОТМЕНИТЬ '),
        state=NewPizzaFSM.all_states + RedactPizzaFSM.all_states + MailingFSM.all_states
        )

    dp.register_message_handler(new_pizza, Text('ДОБАВИТЬ ПИЦЦУ➕'), state=MainAdminFSM.admin_state)
    dp.register_message_handler(get_name, state=NewPizzaFSM.name_state)
    dp.register_message_handler(get_price, state=NewPizzaFSM.price_state)
    dp.register_message_handler(get_descr, state=NewPizzaFSM.descr_state)
    dp.register_message_handler(insert_pizza, state=NewPizzaFSM.image_state)

    dp.register_message_handler(redact_pizza, Text('ИЗМЕНИТЬ ПАРАМЕТРЫ ПИЦЦЫ📝'), state=MainAdminFSM.admin_state)
    dp.register_callback_query_handler(get_pizza, state=RedactPizzaFSM.pizza_state)
    dp.register_callback_query_handler(get_what_change, state=RedactPizzaFSM.what_state)
    dp.register_message_handler(get_change, state=RedactPizzaFSM.change_state)

    dp.register_message_handler(make_mailing, Text('СОЗДАТЬ РАССЫЛКУ ПОЛЬЗОВАТЕЛЯМ✉️'), state=MainAdminFSM.admin_state)
    dp.register_message_handler(get_photo, content_types=['photo'], state=MailingFSM.photo_state)
    dp.register_message_handler(get_text, state=MailingFSM.text_state)
    dp.register_callback_query_handler(add_bt, Text('add_bt'), state=MailingFSM.add_button_state)
    dp.register_message_handler(get_bt_text, state=MailingFSM.button_text_state)
    dp.register_message_handler(get_bt_url, state=MailingFSM.button_url_state)
    dp.register_callback_query_handler(send_mailing, Text('send'), state=MailingFSM.add_button_state)
