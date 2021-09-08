import requests
from bs4 import BeautifulSoup

url = 'https://olimpiada.ru/activity'
activity_id = '1'

url = url.rstrip('/')
response = requests.get(f'{url}/{activity_id}')
soup = BeautifulSoup(response.text, 'lxml')

out = soup.select('#new_for_activity a.new_link:first-child')

print(out[0].text)
