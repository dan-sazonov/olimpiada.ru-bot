import features
import scrapper
import requests

testing = list(range(1, 6)) + [73, 153, 465, 22]

for i in testing:
    url = f'https://olimpiada.ru/activity/{i}'
    title = scrapper.get_title(url)
    status = scrapper.get_status(url)
    date, news_title = scrapper.get_last_news(url)
    calendar = scrapper.get_calendar(url)
    event_title, event_date = features.last_event_info(calendar)
    print(url)
    print(title)
    print(status)
    print(date, end=' ')
    print('' if not date else features.convert_date(date))
    print(news_title)
    print(calendar)
    print(event_title, event_date)

    print()
# url = 'https://olimpiada.ru/activity/2'
#
# print(scrapper.get_title(url))
# print(scrapper.get_last_news(url))
# print(scrapper.get_calender(url))

print(features.validate_url('https://olimpiada.ru/activity/2/fuckbjk/dick'))
print(features.validate_url('https://olimpiada.ru/activity/22'))
print(features.validate_url('https://olimpiada.ru/activity/73'))
print(features.validate_url('https://olimpiada.ru/activity/153'))
print(features.validate_url('1'))
print(features.validate_url('https://olimpiada.ru'))
print(features.validate_url('https://old-sud.ga'))