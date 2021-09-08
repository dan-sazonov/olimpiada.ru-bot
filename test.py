import features

for i in range(1, 6):
    url = f'https://olimpiada.ru/activity/{i}'
    title = features.get_title(url)
    date, news_title = features.get_last_news(url)

    if title and date and news_title:
        print(title)
        print(date)
        print(news_title)

