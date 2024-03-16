# pip install -r pip-requirements.txt

import asyncio
from asyncio import sleep
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from get_message_data import get_telegram_id_users
from config import *
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram import F
from typing import Any, Dict
#####
from add_message_data import add_message_data
import datetime
import pytz
#####

class AddRecordMessage(StatesGroup):
    add_message = State()


@router.message(Command(commands=['start']))
async def add_item(message: types.Message, state: FSMContext):
    await message.answer(text=f'{message.from_user.first_name}, напишите свое сообщение')
    await state.set_state(AddRecordMessage.add_message)


@router.message(AddRecordMessage.add_message)
async def add_item(message: types.Message, state: FSMContext):
    data = await state.update_data(add_message=message.text)
    telegra_id = message.from_user.id
    chat_id = message.chat.id
    await state.clear()
    await add_record(data=data)
    add_message = data["add_message"]
    current_time = datetime.datetime.now()
    desired_timezone = pytz.timezone('Europe/Moscow')
    localized_time = desired_timezone.localize(current_time)
    fulldate = localized_time.strftime("%d-%m-%Y %H:%M:%S%z")  # ???????
    full_date = datetime.datetime.strptime(fulldate, "%d-%m-%Y %H:%M:%S%z")  #???????
    await add_message_data(telegra_id, chat_id, add_message, full_date)
    await message.answer('Ваше сообщение отправлено модератору на рассмотрение. В ближайшее время он с Вами свяжется')

async def add_record(data: Dict[str, Any]) -> None: #??????
    add_message = data["add_message"]


###############

class SendMessage(StatesGroup):
    sending_message = State()
    photo = State()


@router.message(Command(commands=['mailing']))
async def start_mailing(message: types.Message, state: FSMContext):
    #if message.from_user.id == admins:
    await message.answer(f"{message.from_user.first_name}, введите текст рассылки")
    await state.set_state(SendMessage.sending_message)


@router.message(SendMessage.sending_message)
async def mailing_text(message: types.Message, state: FSMContext):
    #if message.from_user.id == admins:
    await state.update_data(sending_message=message.text)
    await message.answer(text='Загрузите фото')
    await state.set_state(SendMessage.photo)


@router.callback_query(F.data == "send")
async def start(call: types.CallbackQuery, state: FSMContext):
    #if call.message.from_user.id == admins:
    users = await get_telegram_id_users()
    data = await state.get_data()
    sending_message = data.get('sending_message')
    photo = data.get('photo')
    await state.clear()
    for user in users:
        # await bot.send_message(chat_id=user, text=sending_message)
        await bot.send_photo(chat_id=user, photo=photo, caption=sending_message)
        await sleep(0.33)
    await call.message.answer('Рассылка выполнена.')


@router.message(SendMessage.photo)
async def mailing_text(message: types.Message, state: FSMContext):
    #if message.from_user.id == admins:
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    sending_message = data.get('sending_message')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отправить', callback_data='send'),
                                          InlineKeyboardButton(text='Отменить', callback_data='cancel')
                                      ]
                                  ])
    await message.answer_photo(photo=photo, caption=sending_message, reply_markup=markup)


@router.callback_query(F.data == "cancel")
async def quit(call: types.CallbackQuery, state: FSMContext):
    #if call.message.from_user.id == admins:
    await state.clear()
    await call.message.answer('Рассылка отменена. Введите новый текст рассылки!!!')
    await state.set_state(SendMessage.sending_message)



async def add_message(data: Dict[str, Any]) -> None:
    sending_message = data["sending_message"]
    photo = data["photo"]


async def main():
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())