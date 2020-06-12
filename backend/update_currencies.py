import asyncio

from currencies.utils import update_currencies


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_currencies())
