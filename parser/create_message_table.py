
import asyncpg
import asyncio
from config import *


async def creat_message_data_table():
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS tele_bot_app_MessageData (
    id serial,
    telegram_id INTEGER,
    chat_id INTEGER,
    message TEXT,
    full_date_time TEXT
    )
    ''')
    await conn.close()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(creat_message_data_table())