import asyncio

import settings
from currencies.utils import update_currencies
from databases import Database

async def get_currencies():
    await database.connect()
    await update_currencies(database)
    await database.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    database = Database(settings.connection)
    loop.run_until_complete(get_currencies())
