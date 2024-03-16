
from aiogram.fsm.state import State, StatesGroup  # библиотека для создания класса в telegram bot
from aiogram import types
from aiogram.fsm.context import FSMContext
from typing import Any, Dict
from add_message_data import add_message_data
from config import *
from aiogram.filters import Command
import asyncio
import datetime
import pytz


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


async def main():
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

