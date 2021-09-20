"""
Features that using database or config it
"""

import sqlite3
import ast
import scrapper
import datetime


class DB:
    def __init__(self):
        """
        Initialize 'events' and 'users' databases if they don't exist and set attributes
        """
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        self.db, self.cursor = db, cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, title TEXT, news_date TIMESTAMP, "
                       "news_title TEXT, calendar TEXT, next_round TEXT, next_date TIMESTAMP, event_status TEXT, "
                       "last_update TIMESTAMP)")
        cursor.execute("CREATE TABLE IF NOT EXISTS users(user INTEGER PRIMARY KEY, ids TEXT)")
        db.commit()

    def select_from_users(self, user_id: int) -> tuple:
        """
        Select ids from the 'users' table by user's id

        :param user_id: user's telegram id and key in the table
        :return: tuple with data from the table
        """
        self.cursor.execute("SELECT ids FROM users WHERE user = :id", {'id': user_id})
        return self.cursor.fetchone()

    def select_from_events(self, event_id: int, cols: list[str]):
        # don't use placeholders in this request, '*' won't work!
        self.cursor.execute(f"SELECT {', '.join(cols)} FROM events WHERE id = {int(event_id)}")
        return self.cursor.fetchone()

    def insert_into_users(self, user_id: int, events: set) -> None:
        """
        Insert into the 'users' table set of event ids

        :param user_id: user's telegram id and key in the table
        :param events: set with event ids
        :return: None
        """
        self.cursor.execute("INSERT OR IGNORE INTO users(user, ids) VALUES(?, ?)", (user_id, str(events)))
        self.db.commit()

    def insert_into_events(self, data: scrapper.Event) -> None:
        tmp = (data.id, data.title, data.last_news_date, data.last_news_title, str(data.calendar),
               data.next_round_title, data.next_round_date, data.status, str(data.last_update))
        self.cursor.execute("INSERT OR IGNORE INTO events(id, title, news_date, news_title, calendar, next_round, "
                            "next_date, event_status, last_update) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", tmp)
        self.db.commit()

    def update_users(self, user_id: int, events: set) -> None:
        """
        Updates the ids in the table for a specific user

        :param user_id: user's telegram id and key in the table
        :param events: set with new event ids
        :return: None
        """
        self.cursor.execute("UPDATE users SET ids = :ids WHERE user = :id", {'ids': str(events), 'id': user_id})
        self.db.commit()


db = DB()


def init_bd():
    return '', ''


def get_events(user_id: int) -> set:
    """
    Return a set of ids of all user events

    :param user_id: user's telegram id
    :return: set of olympiad ids, int
    """
    out = db.select_from_users(user_id)

    return set() if not out else ast.literal_eval(out[0])


def add_events(user_id: int, events: set) -> None:
    """
    Add events to the database for the selected user

    :param user_id: user's telegram id
    :param events: set of olympiad ids, int
    :return: None
    """
    cur_events = get_events(user_id)

    if not cur_events:
        db.insert_into_users(user_id, events)
    else:
        tmp = events.union(cur_events)
        db.update_users(user_id, tmp)


def remove_events(user_id: int, events: set) -> None:
    """
    Remove events from the database for the selected user

    :param user_id: user's telegram id
    :param events: set of olympiad ids, int
    :return: None
    """

    cur_events = get_events(user_id)

    if not cur_events:
        return
    tmp = cur_events - events
    db.update_users(user_id, tmp)


def update_event(event_id: int) -> None:
    """
    Add information about event to the database, or update it, if the calendar or the last news title will be changed.
    If less than 5 and a half hours have passed since the last update, the function will be aborted. If event's id is
    invalid, the err will be raised

    :param event_id: event's id
    :return: None
    """

    event_request = db.select_from_events(event_id, ['*'])
    event = None if not event_request else scrapper.Event(*event_request)

    # abort the function if not enough time has passed
    delta_time = None if not event else (datetime.datetime.now() - event.last_update)
    if delta_time and delta_time.seconds <= 19800 and delta_time.days < 1:
        return

    parsed_data = scrapper.get_event(str(event_id))
    if not event:
        db.insert_into_events(parsed_data)
        return
    else:
        # сравниваем текущую дату новости из бд и календарь с распаршенными, если поменялись - апдейтим ивент
        pass

    # # run parser and get class
    # a = scrapper.Event(event_id)
    # data = (a.id, a.title, a.last_news_date, a.last_news_title, str(a.calendar), a.next_round_title, a.next_round_date,
    #         a.status, datetime.datetime.now())
    #
    # if not fetch:
    #     # add the event
    #     cursor.execute("INSERT OR IGNORE INTO events(id, title, news_date, news_title, calendar, next_round, next_date,"
    #                    "event_status, last_update) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    #     db.commit()
    #     return
    #
    # tmp_last_news_date, tmp_calendar = fetch[2], fetch[4]
    # if tmp_last_news_date != a.last_news_date or tmp_calendar != str(a.calendar):
    #     # update the event
    #     cursor.execute("UPDATE events SET news_date = :nd, news_title = :nt, calendar = :c, next_round = :nr, "
    #                    "next_date = :d, event_status = :es, last_update = :ld WHERE id = :id",
    #                    {'nd': a.last_news_date, 'nt': a.last_news_title, 'c': str(a.calendar),
    #                     'nr': a.next_round_title, 'd': a.next_round_date, 'es': a.status, 'ld': datetime.datetime.now(),
    #                     'id': a.id})
    # db.commit()


# fuck the DRY, I want it like this
def get_statuses(user_id: int) -> list[tuple[str, str]]:
    """
    Return the statuses of all user events

    :param user_id: user's telegram id
    :return: list with pairs 'title', 'status' in the tuples
    """
    db, cursor = init_bd()
    statuses = []

    for event in get_events(user_id):
        cursor.execute("SELECT title, event_status FROM events WHERE id = :id", {'id': event})
        statuses.append(cursor.fetchone())

    return statuses


def get_next_rounds(user_id: int) -> list[tuple[str, str, str]]:
    """
    Return the information about next rounds of all user events

    :param user_id: user's telegram id
    :return: list with tuples ('title', 'round-title', 'date')
    """
    db, cursor = init_bd()
    rounds = []

    for event in get_events(user_id):
        cursor.execute("SELECT title, next_round, next_date FROM events WHERE id = :id", {'id': event})
        tmp = cursor.fetchone()
        if tmp[1] and tmp[2]:
            rounds.append((tmp[0], tmp[1], '.'.join(tmp[2].split('-')[::-1])))

    return rounds


def get_last_news(user_id: int) -> list[tuple[str, str, str]]:
    """
    Return the latest news of all user events

    :param user_id: user's telegram id
    :return: list with tuples ('title', 'news date', 'news title')
    """
    db, cursor = init_bd()
    news = []

    for event in get_events(user_id):
        cursor.execute("SELECT title, news_date, news_title FROM events WHERE id = :id", {'id': event})
        tmp = cursor.fetchone()
        if tmp[1] and tmp[2]:
            news.append((tmp[0], tmp[1], tmp[2]))

    return news


def get_users_events(user_id: int) -> list[tuple[str, str, str]]:
    """
    Return title, id and time of last updating of all user events
    :param user_id: user's telegram id
    :return: list with tuples ('title', 'news date', 'news title')
    """
    db, cursor = init_bd()
    events = []

    for event in get_events(user_id):
        cursor.execute("SELECT title, last_update FROM events WHERE id = :id", {'id': event})
        tmp = cursor.fetchone()
        events.append((event, tmp[0], tmp[1].split()[1].split('.')[0]))

    return events


if __name__ == "__main__":
    init_bd()
