import requests
from bs4 import BeautifulSoup, element


def get_html(url: str, selector: str) -> element.ResultSet:
    """
    Returns the html code by selector and validate the url

    :param url: url that needs to be parsed
    :param selector: CSS-selector of the desired element
    :return: HTML code
    """
    try:
        response = requests.get(url.rstrip('/'))
    except requests.exceptions.ConnectionError or requests.exceptions.MissingSchema:
        # do something if url is wrong
        return BeautifulSoup.ResultSet()
    soup = BeautifulSoup(response.text, 'lxml')

    return soup.select(selector)


def get_title(url: str) -> str:
    """
    Returns the name of the competition by the url

    :param url: url of the competition
    :return: title of this competition
    """
    out = get_html(url, '.headline_activity h1')

    return out[0].text if out else ''


def get_last_news(url: str) -> tuple:
    """
    Returns the title of the latest news about this competition

    :param url: url of the competition
    :return: date of publishing and title of this news: (date, title)
    """
    out = get_html(url, '#new_for_activity a.new_link:first-child')

    if not out:
        return '', ''

    out = out[0].text.split('\n')
    date = out[0].strip('\t').split(', ')[-1]
    title = out[1].strip('\t')

    return date, title


def get_calender(url: str) -> dict:
    """
    Returns calendar with the schedule of this competition

    :param url: url of the competition
    :return: dict: {'name of this round': 'date of the event'}
    """
    i = 0
    calender = dict()

    out = get_html(url, '.left > .events_for_activity')
    if not out:
        return dict()
    out = out[0].select('td > a')

    while i < len(out):
        calender[out[i].text.replace('\xa0', ' ')] = out[i + 1].text.replace('\xa0', ' ')
        i += 2

    return calender
