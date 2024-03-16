
import asyncpg
import asyncio
from config import *


async def get_telegram_id_users():
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    query = await conn.fetch('''SELECT telegram_id FROM tele_bot_app_MessageData''')
    all_records_telegram_id = [record['telegram_id'] for record in query]
    telegram_users = list(set(all_records_telegram_id))
    return telegram_users


# loop = asyncio.get_event_loop()
# print(loop.run_until_complete(get_telegram_id_users()))