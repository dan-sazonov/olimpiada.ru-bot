"""
Main process of the bot
All the functions should be created in other files.
"""

from aiogram import executor
from dispatcher import dp
import asyncio
import handlers

loop = asyncio.get_event_loop()
delay = 10.0


async def my_func():
    await handlers.test_message()
    when_to_call = loop.time() + delay  # delay -- промежуток времени в секундах.
    loop.call_at(when_to_call, my_callback)


def my_callback():
    asyncio.ensure_future(my_func())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=handlers.start_message, on_shutdown=handlers.stop_message)
