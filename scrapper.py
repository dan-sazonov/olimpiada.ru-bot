import requests
# import features
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
        return element.ResultSet('')
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
    Returns the title of the latest news about this competition. If the news title contains link to the article, this
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


def get_calendar(url: str):
    """
    Returns calendar with the schedule of this competition

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
    # сайт, который мы парсим, решил прилечь. За 3 fucking дня до дэдлайна.
    # todo допилю эту фичу, как olimpiada.ru поднимется
    pass
