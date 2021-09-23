"""
Features that can be used in any files, and on the basis of which other functions can be created
"""

from datetime import datetime, date
from bs4 import BeautifulSoup, element
import requests

global_data = {'parsed_page': element.ResultSet, 'last_url': ''}  # bad practise, I know


def get_element(url: str, selector: str) -> element.ResultSet:
    """
    Return the html code by selector and validate the url

    :param url: url that needs to be parsed
    :param selector: CSS-selector of the desired element
    :return: HTML code of this element
    """
    if (not global_data['parsed_page']) or (global_data['last_url'] != url):
        # parse the page if it hasn't been done yet
        try:
            response = requests.get(url.rstrip('/'))
        except requests.exceptions.ConnectionError or requests.exceptions.MissingSchema:
            return element.ResultSet('')

        global_data['last_url'] = url
        global_data['parsed_page'] = BeautifulSoup(response.text, 'lxml').find('body')

    return global_data['parsed_page'].select(selector)


def test_parsing(url: str) -> bool:
    """
    Return true if the page from the url parameter has a valid header

    :param url: url of this page
    :return: bool flag
    """

    return bool(get_element(url, '.headline_activity h1'))


def create_url(event_id: int) -> str:
    """
    Return the correct link to the event by its id

    :param event_id: id of the event
    :return: link to the event
    """
    return f'https://olimpiada.ru/activity/{event_id}'


def validate_url(url: str) -> tuple[str, int]:
    """
    Return correct url and id if getting only id. If url is invalid, returns empty string. Otherwise, returns url

    :param url: url that needs to be validated or id
    :return: (correct url or empty string, id of this event or empty string)
    """
    if url.isdigit():
        url = create_url(int(url))
    if not (url.startswith('https://olimpiada.ru/activity/') and test_parsing(url)):
        return '', 0
    event_id = url.strip('/').split('/')[-1]
    return url, int(event_id)


def convert_date(usr_date: str, is_upcoming=False) -> tuple[datetime.date, bool]:
    """
    Convert a user-friendly date to a datetime object. If this day was already in this year, the value of the year will
    be equal to the current one, otherwise the previous one. If the is_upcoming flag is set to True and this day was
    already in this year before September 1, then the year will be increased by 1. The second parameter return True if
    this date was in this year. If got the empty string, ValueError will be raised

    :param usr_date: user-friendly date in the form of 'day month'
    :param is_upcoming: flag, read the docstring
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
    year -= int(not was_this_date and not is_upcoming)
    year += int((was_this_date and month < 9) and is_upcoming)

    return date(year, month, day), was_this_date


def last_event_info(calendar: list) -> tuple[str, datetime.date]:
    """
    Return the name and date of the next event from the calendar

    :param calendar: list with the pairs title-date in the tuple. Received from the database or get_calendar
    :return: (title, date). If there are no upcoming events, return a tuple with two empty strings
    """
    for event in calendar:
        day, month = (event[1].split()[1], event[1].split()[1]) if event[1].startswith('До') else (
            event[1].split('...')[0], event[1].split()[-1])

        time, already_been = convert_date(f"{day} {month}", is_upcoming=True)
        if not already_been:
            return ' '.join(event[0]), time
    return '', ''
