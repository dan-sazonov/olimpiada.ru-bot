import sqlite3
import ast


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


if __name__ == "__main__":
    init_bd()
