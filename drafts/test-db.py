import sqlite3
import ast
import datetime

db = sqlite3.connect('test.db')
cursor = db.cursor()

# создаем бд с указанными столбцами
cursor.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, title TEXT, news_date TIMESTAMP, "
               "news_title TEXT, news_link TEXT, calender TEXT)")
db.commit()

# записываем инфу по новой олимпиаде
data = (1, 'Четкая олимпиада', datetime.date(2021, 8, 29), 'заголовок новости', 'https://yandex.ru',
        str({'11 сент': '1 этап', }))
cursor.execute("INSERT OR IGNORE INTO events(id, title, news_date, news_title, news_link, calender) "
               "VALUES(?, ?, ?, ?, ?, ?)", data)
db.commit()

# выгружаем всю инфу по иду
target_id = (1,)
cursor.execute("SELECT * FROM events WHERE id = 1")
usr_id, usr_title, usr_news_date, usr_news_title, usr_news_link, usr_calender = cursor.fetchall()[0]
usr_calender = ast.literal_eval(usr_calender)
print(usr_id, usr_title, usr_news_date, usr_news_title, usr_news_link, usr_calender)

# сравниваем текущее значение с новым
target_id_int = 1
new_value = 'новый заголовок новости'  # который добыт парсером
new_date = datetime.date(2021, 8, 29)
new_calender = "{'11 сент': '1 этап',}"
cursor.execute("SELECT news_title FROM events WHERE id = :id", {'id': target_id_int})
if cursor.fetchall()[0][0] != new_value:
    print('Вышла новая новость!')

# апдейтим заголовок новости, дату и календарь
cursor.execute("UPDATE events SET news_date = :d, news_title = :v, calender = :cd WHERE id = :id",
               {'d': new_date, 'v': new_value, 'cd': new_calender, 'id': target_id_int})
db.commit()