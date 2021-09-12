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


def convert_date(usr_date: str) -> (datetime.date, bool):
    """
    Converts a user-friendly date to a datetime object. If this day was already in this year, the value of the year will
    be equal to the current one, otherwise the previous one. The second parameter returns True if this date was in this
    year. If got the empty string, ValueError will be raised

    :param usr_date: user-friendly date in the form of 'day month'
    :return: (datetime.date object with this date, bool flag)
    """
    month_names = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'мая': 5, 'июн': 6, 'июл': 7, 'авг': 8, 'сен': 9, 'окт': 10,
                   'ноя': 11, 'дек': 12}
    day, month = usr_date.split()[:2]
    day = int(day)
    month = month_names[month.lower()[:3]]
    year = datetime.date(datetime.now()).year

    cur_month = datetime.date(datetime.now()).month
    cur_day = datetime.date(datetime.now()).day
    was_this_date = (month < cur_month) or (month == cur_month and day <= cur_day)
    year -= not was_this_date

    return date(year, month, day), was_this_date


def last_event_info(calendar: list) -> (str, datetime.date):
    """
    Returns the name and date of the next event from the calendar

    :param calendar: list with the pairs title-date in the tuple. Received from the database or get_calendar
    :return: (title, date). If there are no upcoming events, returns a tuple with two empty strings
    """
    for event in calendar:
        time, already_been = convert_date(f"{event[1].split('...')[0]} {event[1].split()[-1]}")
        if not already_been:
            return event[0], time
    return '', ''
