import logging
import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv('BOT_TOKEN')
if not API_TOKEN:
    exit('Err: BOT_TOKEN variable is missing')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Простой эхо-бот, который будет постепенно допиливаться")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
