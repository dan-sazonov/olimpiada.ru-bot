import features
import scrapper

testing = list(range(1, 6)) + [73, 153, 465]

for i in range(1, 6):
    url = f'https://olimpiada.ru/activity/{i}'
    title = scrapper.get_title(url)
    date, news_title = scrapper.get_last_news(url)
    calender = scrapper.get_calender(url)
    if title and date and news_title:
        print(title)
        print(date)
        print(news_title)
        if calender:
            print(calender)

        print()
# url = 'https://olimpiada.ru/activity/2'
#
# print(scrapper.get_title(url))
# print(scrapper.get_last_news(url))
# print(scrapper.get_calender(url))
