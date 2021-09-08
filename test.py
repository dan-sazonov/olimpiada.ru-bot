import features

for i in range(1, 6):
    title = features.get_title(f'https://olimpiada.ru/activity/{i}')
    if title:
        print(title)
