import datetime
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


def convert_date(date: str) -> datetime.date:
    """
    Returns some fucking piece of shit

    :param date:
    :return:
    """
    # сайт, который мы парсим, решил прилечь. За 3 fucking дня до дэдлайна.
    # todo допилю эту фичу, как olimpiada.ru поднимется
    pass
