import requests
from bs4 import BeautifulSoup


def get_html(url, selector):
    response = requests.get(url.rstrip('/'))
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
