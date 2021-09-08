import requests
from bs4 import BeautifulSoup


def get_title(url):
    response = requests.get(url.rstrip('/'))
    soup = BeautifulSoup(response.text, 'lxml')

    out = soup.select('.headline_activity h1')

    return out[0].text if out else None
