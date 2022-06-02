from time import sleep

import requests
import pandas as pd

from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.2228.0 Safari/537.36'}



def get_html(streamer):
    r = requests.get(f'https://twitchtracker.com/{streamer}/games', headers=HEADERS)
    return r


def get_content(html, streamer):
    '''Используем КрасивыйСуп для получения данных со страницы игр стримера'''

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    items = table.find_all('tr')
    items.pop(0)  # Удаляем первый элемент, так как он пустой
    columns = ['Game', 'Avg. viewers', 'Max. viewers', 'Followers/hour', 'Stream time (hours)', 'Last seen']
    df = pd.DataFrame(columns=columns)
    for item in items:
        names = item.find('a')

        '''Проверяем название игр на ненужные категории'''

        if names.get_text() == 'Games + Demos' or names.get_text() == 'IRL' or names.get_text() == 'Twitch Plays' or names.get_text() == 'Just Chatting' or names.get_text() == 'Art':
            continue

        else:
            name = item.find('a').get_text()
            viewers = item.find_all('span')[0].get_text()
            max_viewers = item.find_all('span')[1].get_text()
            followers = item.find_all('span')[2].get_text()
            time = item.find_all('span')[3].get_text()
            date = item.find_all('span')[4].get_text()

            '''Загружаем в значение каждой игры в таблицу при помощи Pandas'''

            df1 = pd.DataFrame([[
                name,
                int(viewers),
                int(max_viewers),
                float(followers),
                round(float(time) / 60, 1),
                date
            ]], columns=columns)

            df = pd.concat([df, df1])

    df.to_excel(f'{streamer}_statistic.xlsx', index=False)  # Создаем xlsx файл с таблицей
    print(f'Файл {streamer}_statistic.xlsx сохранен!')


def parse():
    streamer = input('Введите название канала (или exit для выхода): ')
    if streamer == 'exit':
        print('Всего хорошего!')
    else:
        html = get_html(streamer)

        if html.status_code == 200:
            print('Процесс получения статистики запущен...')
            get_content(html.text, streamer)

        else:
            print('Error - Что-то пошло не так')


if __name__ == "__main__":
    parse()
    sleep(5)