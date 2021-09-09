import features

testing = list(range(1, 6)) + [73, 153, 465]

# for i in range(1, 6):
#     url = f'https://olimpiada.ru/activity/{i}'
#     title = features.get_title(url)
#     date, news_title = features.get_last_news(url)
#     calender = features.get_calender(url)
#
#     if title and date and news_title:
#         print(title)
#         print(date)
#         print(news_title)
#         if calender:
#             print(calender)
#
#         print()
url = 'http://old-sud.ga'

print(features.get_last_news(url))
print(features.get_last_news(url))
print(features.get_calender(url))
