from aiogram import types
from dispatcher import dp, bot
import config


async def start_message(_):
    await bot.send_message(chat_id=config.ADMIN_ID, text='Бот запущен')


async def stop_message(_):
    await bot.send_message(chat_id=config.ADMIN_ID, text='Бот остановлен')


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Простой эхо-бот, который будет постепенно допиливаться")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
