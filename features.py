import requests
from bs4 import BeautifulSoup


def get_html(url, selector):
    try:
        response = requests.get(url.rstrip('/'))
    except requests.exceptions.ConnectionError or requests.exceptions.MissingSchema:
        # do something if url is wrong
        return ''
    soup = BeautifulSoup(response.text, 'lxml')

    return soup.select(selector)


def get_title(url):
    out = get_html(url, '.headline_activity h1')

    return out[0].text if out else None


def get_last_news(url):
    out = get_html(url, '#new_for_activity a.new_link:first-child')

    if not out:
        return None, None

    out = out[0].text.split('\n')
    date = out[0].strip('\t').split(', ')[-1]
    title = out[1].strip('\t')

    return date, title


def get_calender(url):
    i = 0
    calender = dict()

    out = get_html(url, '.left > .events_for_activity')
    if not out:
        return None
    out = out[0].select('td > a')

    while i < len(out):
        calender[out[i].text.replace('\xa0', ' ')] = out[i + 1].text.replace('\xa0', ' ')
        i += 2

    return calender
