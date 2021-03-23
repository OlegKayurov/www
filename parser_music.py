import requests
from bs4 import BeautifulSoup as bs

link = 'https://ruv.hotmo.org/genre/6'

b = 'Rammstein'
page = '/start/'

def music_pars():
    for i in range(0, 600, 48):
        pages = f'{page}{i}'
        r = requests.get(f'{link}{pages}').text
        soup = bs(r, 'html.parser')
        block = soup.find('div', class_='content-inner')
        all_music = block.find_all('div', class_='track__info-r')
        for music in all_music:
            music_link = music.find('a').get('href')

            if b in music_link:
                print(music_link)
                Rammstein = music_link[41:]
                music_bytes = requests.get(music_link).content
                try:
                    with open('music_links.txt', 'a', newline='') as f:
                        f.write(music_link)
                except:
                    print('error')
                try:
                    with open(f'music/{Rammstein}', 'wb') as file:
                        file.write(music_bytes)
                    print(f'music {Rammstein} loading is complete')
                except:
                    print('error')

print(music_pars())

