from aiogram.enums import ParseMode
import os
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)
router = Router()

admins = os.getenv('ADMIN_ID')

host = os.getenv('IP')
user = str(os.getenv('POSTGRES_USER'))
password = str(os.getenv('POSTGRES_PASSWORD'))
database = str(os.getenv('POSTGRES_DATABASE'))


POSTGRES_URI = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
print(f"{POSTGRES_URI=}")


