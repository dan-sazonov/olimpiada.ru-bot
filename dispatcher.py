import logging
import os
from aiogram import Bot, Dispatcher
import config

API_TOKEN = os.getenv('BOT_TOKEN')
if not API_TOKEN:
    exit('Err: BOT_TOKEN variable is missing')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
