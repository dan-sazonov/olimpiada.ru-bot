from datetime import datetime, date
from scrapper import get_title


def validate_url(url: str) -> (str, int):
    """
    Returns correct url and id if getting only id. If url is invalid, returns empty string. Otherwise, returns url

    :param url: url that needs to be validated or id
    :return: (correct url or empty string, id of this event or empty string)
    """
    if url.isdigit():
        event_id = url
        url = f'https://olimpiada.ru/activity/{event_id}'
    if not (url.startswith('https://olimpiada.ru/activity/') and get_title(url)):
        return '', 0
    event_id = url.strip('/').split('/')[-1]
    return url, int(event_id)


def convert_date(usr_date: str) -> datetime.date:
    """
    Converts a user-friendly date to a datetime object. If this day was already in this year, the value of the year will
     be equal to the current one, otherwise the previous one. If got the empty string, ValueError will be raised

    :param usr_date: user-friendly date in the form of 'day month'
    :return: datetime.date object with this date
    """
    month_names = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'мая': 5, 'июн': 6, 'июл': 7, 'авг': 8, 'сен': 9, 'окт': 10,
                   'ноя': 11, 'дек': 12}
    day, month = usr_date.split()
    day = int(day)
    month = month_names[month.lower()[:3]]
    year = datetime.date(datetime.now()).year

    cur_month = datetime.date(datetime.now()).month
    cur_day = datetime.date(datetime.now()).day
    year -= 1 if (month > cur_month) or (month == cur_month and day > cur_day) else 0

    return date(year, month, day)
