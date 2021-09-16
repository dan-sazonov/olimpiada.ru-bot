"""
Features that using database or config it
"""

import sqlite3
import ast
import scrapper


def init_bd() -> (sqlite3.Connection, sqlite3.Cursor):
    """
    Initialize 'events' and 'users' databases if they don't exist

    :return: (Connection db object, Cursor db.object)
    """
    db = sqlite3.connect('main.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, title TEXT, news_date TIMESTAMP, "
                   "news_title TEXT, calendar TEXT, next_round TEXT, next_date TIMESTAMP, event_status TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users(user INTEGER PRIMARY KEY, ids TEXT)")
    db.commit()

    return db, cursor


def get_events(user_id: int) -> set:
    """
    Return a set of ids of all user olympiads

    :param user_id: user's telegram id
    :return: set of olympiad ids, int
    """
    db, cursor = init_bd()
    cursor.execute("SELECT * FROM users WHERE user = :id", {'id': user_id})

    if not cursor.fetchone():
        return set()
    else:
        cursor.execute("SELECT * FROM users WHERE user = :id", {'id': user_id})
        return ast.literal_eval(cursor.fetchone()[1])


def add_events(user_id: int, events: set) -> None:
    """
    Add events to the database for the selected user

    :param user_id: user's telegram id
    :param events: set of olympiad ids, int
    :return: None
    """
    db, cursor = init_bd()
    cursor.execute("SELECT * FROM users WHERE user = :id", {'id': user_id})

    if not cursor.fetchone():
        cursor.execute("INSERT OR IGNORE INTO users(user, ids) VALUES(?, ?)", (user_id, str(events)))
    else:
        cursor.execute("SELECT * FROM users WHERE user = :id", {'id': user_id})
        tmp = events.union(ast.literal_eval(cursor.fetchone()[1]))
        events = events.union(tmp)
        cursor.execute("UPDATE users SET ids = :ids WHERE user = :id", {'ids': str(events), 'id': user_id})

    db.commit()


def remove_events(user_id: int, events: set) -> None:
    """
    Remove events from the database for the selected user

    :param user_id: user's telegram id
    :param events: set of olympiad ids, int
    :return: None
    """

    db, cursor = init_bd()
    cursor.execute("SELECT * FROM users WHERE user = :id", {'id': user_id})

    if not cursor.fetchone():
        return
    else:
        cursor.execute("SELECT * FROM users WHERE user = :id", {'id': user_id})
        tmp = str(ast.literal_eval(cursor.fetchone()[1]) - events)
        cursor.execute("UPDATE users SET ids = :ids WHERE user = :id", {'ids': tmp, 'id': user_id})

    db.commit()


def update_event(event_id: str) -> None:
    """
    Add information about event to the database, or update it, if the calendar or the last news title will be changed.
    If event's id is invalid, the err will be raised

    :param event_id: event's id
    :return: None
    """
    a = scrapper.ParsedEvent(event_id)
    data = (a.id, a.title, a.last_news_date, a.last_news_title, str(a.calendar), a.next_round_title, a.next_round_date,
            a.status)

    db, cursor = init_bd()
    cursor.execute("SELECT * FROM events WHERE id = :id", {'id': int(event_id)})

    if not cursor.fetchone():
        # add the event
        cursor.execute("INSERT OR IGNORE INTO events(id, title, news_date, news_title, calendar, next_round, next_date,"
                       "event_status) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)
    else:
        cursor.execute("SELECT * FROM events WHERE id = :id", {'id': int(event_id)})
        f = cursor.fetchone()
        tmp_last_news_date, tmp_calendar = f[2], f[4]
        if tmp_last_news_date != a.last_news_date or tmp_calendar != str(a.calendar):
            # update the event
            cursor.execute("UPDATE events SET news_date = :nd, news_title = :nt, calendar = :c, next_round = :nr, "
                           "next_date = :d, event_status = :es WHERE id = :id",
                           {'nd': a.last_news_date, 'nt': a.last_news_title, 'c': str(a.calendar),
                            'nr': a.next_round_title, 'd': a.next_round_date, 'es': a.status, 'id': a.id})
    db.commit()


def get_statuses(user_id: int) -> dict:
    pass


if __name__ == "__main__":
    init_bd()
