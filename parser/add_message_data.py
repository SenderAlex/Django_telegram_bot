
import asyncpg
import asyncio
from config import *


async def add_message_data(telegram_id, chat_id, message, full_date_time):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''INSERT INTO tele_bot_app_MessageData (telegram_id, chat_id, message, full_date_time)
                        VALUES ($1, $2, $3, $4)''', telegram_id, chat_id, message, full_date_time)
    await conn.close()


# loop = asyncio.get_event_loop()
# loop.run_until_complete(add_message_data(1243423, 42324233,'hello'))