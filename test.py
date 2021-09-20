"""
File with manual tests of some features. Will be deleted in production.
"""

import features
import scrapper
import requests

testing = list(range(1, 6)) + [73, 153, 465, 22, 5283]

for i in testing:
    article = scrapper.get_event('2')

    print(article.id, article.url)
    print(article.title)
    print(article.last_news_date, article.last_news_title)
    print(article.calendar)
    print(article.next_round_date, article.next_round_title)
    break

    # url = f'https://olimpiada.ru/activity/{i}'
    # title = scrapper.get_title(url)
    # status = scrapper.get_status(url)
    # date, news_title = scrapper.get_last_news(url)
    # calendar = scrapper.get_calendar(url)
    # event_title, event_date = features.last_event_info(calendar)
    # print(url)
    # print(title)
    # print(status)
    # print(date, end=' ')
    # print('' if not date else features.convert_date(date))
    # print(news_title)
    # print(calendar)
    # print(event_title, event_date)
    #
    # print()
# url = 'https://olimpiada.ru/activity/2'
#
# print(scrapper.get_title(url))
# print(scrapper.get_last_news(url))
# print(scrapper.get_calender(url))

# print(features.validate_url('https://olimpiada.ru/activity/2/fuckbjk/dick'))
# print(features.validate_url('https://olimpiada.ru/activity/153'))
# print(scrapper.get_title(features.validate_url('1')[0]))
# print(features.validate_url('https://olimpiada.ru/activity/73'))
# print(features.validate_url('https://olimpiada.ru/activity/22'))
# print(features.validate_url('1'))
# print(features.validate_url('https://olimpiada.ru'))
# print(features.validate_url('https://old-sud.ga'))
