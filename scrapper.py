"""
Features that process data received from the parser
Also this file can contain classes for organizing this data.
"""
import features
import datetime

get_element = features.get_element  # parser


class Event(object):
    def __init__(self, e_id: int, title='', last_news_date='', last_news_title='', calendar='', next_round_title='',
                 next_round_date='', status='', last_update=datetime.datetime.now()):
        """
        Information about the event as in the database

        :param e_id: id of this event
        """
        self.id = e_id
        self.url = features.create_url(self.id)
        self.title = title
        self.last_news_date, self.last_news_title = last_news_date, last_news_title
        self.calendar = calendar
        self.next_round_title, self.next_round_date = next_round_title, next_round_date
        self.status = status
        self.last_update = datetime.datetime.fromisoformat(str(last_update))


def get_title(url: str) -> str:
    """
    Return the name of the competition by the url

    :param url: url of the competition
    :return: title of this competition
    """
    out = get_element(url, '.headline_activity h1')

    return out[0].text if out else ''


def get_last_news(url: str) -> tuple[str, str]:
    """
    Return the title of the latest news about this competition. If the news title contains link to the article, this
    link will be added to the title

    :param url: url of the competition
    :return: date of publishing and title of this news: (date, title)
    """
    out = get_element(url, '#new_for_activity a.new_link:first-child')

    if not out:
        return '', ''

    link = out[0].attrs["href"]
    out = out[0].text.split('\n')
    date = out[0].strip('\t').split(', ')[-1]
    title = out[1].strip('\t') if link.startswith('/news') else out[1].strip('\t') + f': https://olimpiada.ru{link}'

    return date, title


def get_calendar(url: str) -> list[tuple[list, str]]:
    """
    Return calendar with the schedule of this competition

    :param url: url of the competition
    :return: dict: {'name of this round': 'date of the event'}
    """
    i = 0
    calendar = list()

    out = get_element(url, '.left > .events_for_activity')
    if not out:
        return list()
    out = out[0].select('td > a')

    while i < len(out):
        calendar.append(([out[i].text.replace('\xa0', ' ')], out[i + 1].text.replace('\xa0', ' ')))
        i += 2

    return calendar


def get_status(url: str) -> str:
    """
    Return the current status of this competition

    :param url: url of the competition
    :return: current status
    """
    out = get_element(url, '.headline_activity a.red')

    return out[0].text.rstrip(' →') if out else ''


def get_event(url: str) -> Event:
    """
    Parse the event page and return the class with all the information

    :param url: url or id of the page
    :return: Event class with parsed information
    """
    url, event_id = features.validate_url(url)
    event = Event(event_id)
    if not event_id:
        return event

    event.title = get_title(url)
    event.last_news_date, event.last_news_title = get_last_news(url)
    event.calendar = get_calendar(url)
    event.next_round_title, event.next_round_date = features.last_event_info(event.calendar)
    event.status = get_status(url)
    event.last_update = datetime.datetime.now()

    return event
