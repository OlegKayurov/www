import csv
import requests
from bs4 import BeautifulSoup as bs
import mysql.connector as sql
import string
import pandas as pd

#добавление записей в БД
def save(cur, con, link, brend1, form_price):

    cur.execute(f""" INSERT INTO Parsing(links, brends, prices) VALUES('{link}', '{brend1}', '{form_price}') """)
    print(f"{'-'*10}\nData added.\n{'-'*10}")

    con.commit()

#Удаление записей
def delete(cur, con):
    #cur.execute("""DELETE FROM Parsing WHERE id=id""")
    cur.execute("""DROP TABLE Parsing""")
    con.commit()
    print(f"{'-' * 10}\nRecording remowed.\n{'-' * 10}")

#Вывод всей таблицы
def view_all(cur):
    cur.execute("""select * from Parsing""")
    for i in iter(cur):
        print(i)

#Фильтрация товара по бренду
def filtr(cur):

    i = input('Введите бренд: ')

    cur.execute(f"""select * from Parsing where brends='{i}'""")

    f = open("Filtr.txt", "w")
    # Get data in batches
    while True:
        # Read the data
        df = pd.DataFrame(cur.fetchmany(1000))
        # We are done if there are no data
        if len(df) == 0:
            break
        # Let's write to the file
        else:
            df.to_csv(f, header=False)

    # Clean up
    f.close()


#запись данных в csv файл
def save_scv(cur, con):

    f = open('output.txt', 'w')

    cur.execute('select * from Parsing')

    while True:
        df = pd.DataFrame(cur.fetchmany(1000))
        if len(df) == 0:
            break
        else:
            df.to_csv(f, header=False)

    # Clean up
    f.close()
    cur.close()
    con.commit()


def main():
    con = sql.connect(host='localhost', user='root', password='root', database='datapars')
    cur = con.cursor()
    #Создание таблицы если ее нет
    cur.execute("""CREATE TABLE IF NOT EXISTS Parsing (id int(50) not null auto_increment primary key,
    links varchar(100), 
    brends varchar(100),
    prices varchar(100))""")
    con.commit()

    while True:
        act = input('Select action:\n'
                    '"Pars" - A\n'
                    '"Delete" - D\n'
                    '"View full list" - F\n'
                    '"Filtr" - I\n'
                    '"Save to Excel" - E\n'
                    
                    '"Exit" - Q\n').lower()
        if act == 'a':
            while True:
                url = 'https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki'
                r = requests.get(url).text
                soup = bs(r, 'lxml')
                links = soup.find('div', class_='catalog_main_table j-products-container')
                all_links = links.find_all('div', class_='dtList i-dtList j-card-item')
                for i in all_links:
                    link = f"{'https://www.wildberries.ru'}{i.find('a').get('href')}"
                    brend = i.find('strong', class_='brand-name c-text-sm').text
                    brend1 = brend.replace('/', '').replace(' ', '')
                    price = i.find('span', class_='price').text
                    #price2 = price.replace('\n', '')
                    valid_characters = string.printable
                    start_string = f"{price}"
                    price2 = ''.join(i for i in start_string if i in valid_characters).replace('\n', '')
                    valid_characters = string.printable
                    start_string = f"{price2}"
                    end_string = ''.join(i for i in start_string if i in valid_characters)
                    form_price = f'new price- {end_string[0:5]}P, old price- {end_string[5:10]}P,' \
                                 f' discount {end_string[10:]}'
                    save(cur, con, link, brend1, form_price)
                break
        else:
            if act == 'd':
                delete(cur, con)
            else:
                if act == 'f':
                    view_all(cur)
                else:
                    if act == 'i':
                        filtr(cur)
                    else:
                        if act == 'e':
                            save_scv(cur, con)
                        else:
                            if act == 'q':
                                break

if __name__=='__main__':
    main()