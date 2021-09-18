"""
Features that use the parser and get some content from the site
Also this file can contain classes for organizing this data.
"""

import requests
import features
from bs4 import BeautifulSoup, element

global_data = {'parsed_page': element.ResultSet, 'last_url': ''}  # bad practise, I know


def get_html(url: str, selector: str) -> element.ResultSet:
    """
    Return the html code by selector and validate the url

    :param url: url that needs to be parsed
    :param selector: CSS-selector of the desired element
    :return: HTML code of this element
    """
    global global_data

    if (not global_data['parsed_page']) or (global_data['last_url'] != url):
        # parse the page if it hasn't been done yet
        global_data['last_url'] = url
        try:
            response = requests.get(url.rstrip('/'))
        except requests.exceptions.ConnectionError or requests.exceptions.MissingSchema:
            # do something if url is wrong
            return element.ResultSet('')
        global_data['parsed_page'] = BeautifulSoup(response.text, 'lxml').find('body')

    return global_data['parsed_page'].select(selector)


def get_title(url: str) -> str:
    """
    Return the name of the competition by the url

    :param url: url of the competition
    :return: title of this competition
    """
    out = get_html(url, '.headline_activity h1')

    return out[0].text if out else ''


def get_last_news(url: str) -> tuple[str, str]:
    """
    Return the title of the latest news about this competition. If the news title contains link to the article, this
    link will be added to the title

    :param url: url of the competition
    :return: date of publishing and title of this news: (date, title)
    """
    out = get_html(url, '#new_for_activity a.new_link:first-child')

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

    out = get_html(url, '.left > .events_for_activity')
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
    out = get_html(url, '.headline_activity a.red')

    return out[0].text.rstrip(' →') if out else ''


class Event(object):
    def __init__(self, url: str, title='', last_news_date='', last_news_title='', calendar='', next_round_title='',
                 next_round_date='', status=''):
        """
        Parse the event and set the class attributes

        :param url: url or id of this event
        """
        # validate url or id, create attributes
        self.url, self.id = features.validate_url(url)

        if any((title, last_news_date, last_news_title, calendar, next_round_title, next_round_date, status)):
            # set attributes based on the received values
            self.title = title
            self.last_news_date, self.last_news_title = last_news_date, last_news_title
            self.calendar = calendar
            self.next_round_title, self.next_round_date = next_round_title, next_round_date
            self.status = status
        else:
            # set the attributes based on received data from the parser
            self.title = get_title(self.url)
            self.last_news_date, self.last_news_title = get_last_news(self.url)
            self.calendar = get_calendar(self.url)
            self.next_round_title, self.next_round_date = features.last_event_info(self.calendar)
            self.status = get_status(self.url)
