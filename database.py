import sqlite3


def init_bd() -> (sqlite3.Connection, sqlite3.Cursor):
    """
    Initialize 'events' and 'users' databases if they don't exist

    :return: (Connection db object, Cursor db.object)
    """
    db = sqlite3.connect('main.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, title TEXT, news_date TIMESTAMP, "
                   "news_title TEXT, news_link TEXT, calender TEXT, next_event TEXT, next_date TIMESTAMP, "
                   "event_status TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users(user INTEGER PRIMARY KEY, ids TEXT)")

    return db, cursor
