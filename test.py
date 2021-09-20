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