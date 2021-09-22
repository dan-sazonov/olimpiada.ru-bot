"""
Handlers of the telegram bot
This file may contain functions that are responsible for the visual display and validation of data. The rest should be
moved to other files: `features` or `database`.
"""

from aiogram import types
from dispatcher import dp, bot
import config
import database


class MessagesText:
    """
    Text of messages sending by the bot
    """

    def __init__(self, user_id=0, event_id=0):
        """
        Create attributes that include the message text
        """
        self.user_events = database.UserEvents(user_id)
        self.db_event = database.DbEvent(event_id)

        self.start_polling = 'Бот запущен'
        self.stop_polling = 'Бот остановлен'
        self.help = 'Простой эхо-бот, который будет постепенно допиливаться'
        self.add_events = 'Введите иды олимпух или ссылки на каждую из них, по одной на строке'
        self.add_events_done = 'Добавлено!'
        self.add_events_failed = 'С дюбавлением некотрых ивентов возникли ошибки. Посмотрите все свои олимпухи, чтобы' \
                                 ' понять, что к чему'
        self.del_events = 'Введите иды олимпух или ссылки на каждую из них, по одной на строке'
        self.del_events_done = 'Удалено!'
        self.del_events_failed = 'С удалением некотрых ивентов возникли ошибки. Посмотрите все свои олимпухи, чтобы' \
                                 ' понять, что к чему'
        # self.last_news = ''
        # self.all_events = ''
        # self.calendar = ''

    def statuses(self):
        ans = ['Статусы олимпух:']
        for event in self.user_events.get_statuses():
            ans.append(f'{event[0]} - {event[1].lower()}.')
        return '\n'.join(ans)

    def next_rounds(self):
        ans = ['Предстоящие мероприятия:']
        for event in self.user_events.get_next_rounds():
            ans.append(f'{event[0]}: {event[1]} - {event[2]}')
        return '\n'.join(ans)


messages = MessagesText(user_id=1)
print(messages.next_rounds())


async def start_message(_):
    await bot.send_message(chat_id=config.ADMIN_ID, text=messages.start_polling)


async def stop_message(_):
    await bot.send_message(chat_id=config.ADMIN_ID, text=messages.stop_polling)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(messages.help)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
