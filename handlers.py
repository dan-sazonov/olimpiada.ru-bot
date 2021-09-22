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

    def __init__(self):
        """
        Create attributes that include the message text
        """
        self.user_events = database.UserEvents
        self.db_event = database.DbEvent

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

    def statuses(self, user_id: int):
        user_events = self.user_events(user_id)
        ans = ['Статусы олимпух:']
        for event in user_events.get_statuses():
            ans.append(f'{event[0]} - {event[1].lower()}.')
        return '\n'.join(ans)

    def next_rounds(self, user_id: int):
        user_events = self.user_events(user_id)
        ans = ['Предстоящие мероприятия:']
        for event in user_events.get_next_rounds():
            ans.append(f'{event[0]}: {event[1]} - {event[2]}')
        return '\n'.join(ans)

    def last_news(self, user_id: int):
        user_events = self.user_events(user_id)
        ans = ['Последние новости:']
        for event in user_events.get_last_news():
            ans.append(f'{event[0]}\n{event[1]}: {event[2]}\n')
        return '\n'.join(ans)

    def all_events(self, user_id: int):
        user_events = self.user_events(user_id)
        ans = ['ID олимпиады, ее название и время последенего обновления:']
        for event in user_events.get_users_events():
            ans.append(f'{event[0]}: "{event[1]}", {event[2]}')
        return '\n'.join(ans)

    def calendar(self, event_id: int):
        db_event = self.db_event(event_id)
        ans = ['Расписание данной олимпиады:']
        for round_ in db_event.get_calendar():
            ans.append(f'{round_[0][0]}: {round_[1]}')
        return '\n'.join(ans)


messages = MessagesText()


async def start_message(_):
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.start_polling)


async def stop_message(_):
    await bot.send_message(chat_id=config.ADMIN_CHAT, text=messages.stop_polling)


@dp.message_handler(commands='statuses')
async def statuses_messages(message: types.Message):
    await message.answer(messages.statuses(message.from_user.id))


@dp.message_handler(commands='next')
async def statuses_messages(message: types.Message):
    await message.answer(messages.next_rounds(message.from_user.id))


@dp.message_handler(commands='news')
async def statuses_messages(message: types.Message):
    await message.answer(messages.last_news(message.from_user.id))


@dp.message_handler(commands='my_events')
async def statuses_messages(message: types.Message):
    await message.answer(messages.all_events(message.from_user.id))


@dp.message_handler(commands='schedule')
async def statuses_messages(message: types.Message):
    await message.answer(messages.calendar(465))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(messages.help)
