from bs4 import BeautifulSoup
import requests
# prob
# Currency parser
def adress(html):
    response = requests.get(html).text
    html = BeautifulSoup(response, 'lxml')
    list_v = html.find_all('a', {'class': 'home-link home-link_black_yes inline-stocks__link'})
    list_f = html.find_all('span', {'class': 'inline-stocks__value_inner'})
    for k, v in zip(list_f, list_v):
        print(k.text, v.text)


def main():
    adress('https://yandex.ru/')


if __name__ == '__main__':
    main()

