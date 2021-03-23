import requests
from bs4 import BeautifulSoup as bs

link = 'https://wallscloud.net/category/anime'

dop = '/1920x1080/download'
image_number = 0
nomer = 0
pg = "?page="
seet = set()
#fail = 'ff.txt'


def handler():
    image_number = 0
    nomer = 0
    for number in range(16):
        nomer += 1
        pages = f'{pg}{nomer}'
        r = requests.get(f'{link}{pages}').text
        soup = bs(r, 'html.parser')
        block = soup.find('div', class_='container-fluid items')
        all_image = block.find_all('div', class_='item')

        for image in all_image:
            image_link = image.find('a').get('href')
            images = f'{image_link}{dop}'
            seet.add(images)

            image_bytes = requests.get(f'{images}').content

            try:
                with open(f'image/{image_number}.jpg', 'wb') as file:
                    file.write(image_bytes)

                image_number += 1
                print(f'images {image_number}.jpg loading is complete ')
            except:
                print('error')
            try:
                with open('ff.txt', 'a', newline='') as f:
                    f.write('/n'.join(seet).join('/n'))
            except:
                print('error')

