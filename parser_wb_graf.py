import requests
from bs4 import BeautifulSoup as bs
from PyQt5 import QtWidgets, uic
import parser_wb, dell
import sys
import mysql.connector as sql
import string
import pandas as pd

class ExampleApp(QtWidgets.QMainWindow, parser_wb.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.parser_and_add_base)
        self.pushButton_2.clicked.connect(self.view_all)
        self.pushButton_3.clicked.connect(self.open_dell)
        self.pushButton_4.clicked.connect(self.filtr)
        self.pushButton_5.clicked.connect(self.print)

    def parser_and_add_base(self):
        self.con = sql.connect(host='localhost', user='root', password='root', database='datapars')
        self.cur = self.con.cursor()
        # Создание таблицы если ее нет
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Parsing (id int(50) not null auto_increment primary key,
                            links varchar(100), 
                            brends varchar(100),
                            prices varchar(100))""")
        self.con.commit()
        self.url = 'https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki'
        self.r = requests.get(self.url).text
        self.soup = bs(self.r, 'lxml')
        self.links = self.soup.find('div', class_='catalog_main_table j-products-container')
        self.all_links = self.links.find_all('div', class_='dtList i-dtList j-card-item')
        for self.i in self.all_links:
            self.link = f"{'https://www.wildberries.ru'}{self.i.find('a').get('href')}"
            self.brend = self.i.find('strong', class_='brand-name c-text-sm').text
            self.brend1 = self.brend.replace('/', '').replace(' ', '')
            self.price = self.i.find('span', class_='price').text
            # price2 = price.replace('\n', '')
            self.valid_characters = string.printable
            self.start_string = f"{self.price}"
            self.price2 = ''.join(i for i in self.start_string if i in self.valid_characters).replace('\n', '')
            self.valid_characters = string.printable
            self.start_string = f"{self.price2}"
            self.end_string = ''.join(i for i in self.start_string if i in self.valid_characters)
            self.form_price = f'new price- {self.end_string[0:5]}P, old price- {self.end_string[5:10]}P,' \
                         f' discount {self.end_string[10:]}'
            self.cur.execute(f""" INSERT INTO Parsing(links, brends, prices) VALUES('{self.link}', '{self.brend1}', '{self.form_price}') """)
            #print(f"{'-' * 10}\nData added.\n{'-' * 10}")
            self.con.commit()

    def view_all(self):
        self.con = sql.connect(host='localhost', user='root', password='root', database='datapars')
        self.cur = self.con.cursor()
        try:
            self.textEdit_2.clear()
            self.cur.execute("""select * from Parsing""")
            for i in iter(self.cur):
                self.textEdit_2.append(f"{i[1]}{'-'*5}{i[2]}{'-'*5}{i[3]}")
        except AttributeError:
            pass

    def filtr(self):
        self.textEdit_2.clear()
        name = self.lineEdit.text()

        self.cur.execute(f"""select * from Parsing where brends='{name}'""")
        for i in iter(self.cur):
            self.textEdit_2.append(f"{i[1]}{'-' * 5}{i[2]}{'-' * 5}{i[3]}")

    def print(self):
        f = open('save_all_data.csv', 'w')
        self.cur.execute('select * from Parsing')
        while True:
            df = pd.DataFrame(self.cur.fetchmany(1000))
            if len(df) == 0:
                break
            else:
                df.to_csv(f, header=False)
        f.close()
        self.cur.close()
        self.con.commit()

    def open_dell(self):
        dialog = Delete()
        dialog.exec_()


class Delete(QtWidgets.QDialog, dell.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.con = sql.connect(host='localhost', user='root', password='root', database='datapars')
        self.cur = self.con.cursor()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.delete_data)

    def delete_data(self):
        self.cur.execute("""DROP TABLE Parsing""")
        self.con.commit()
        self.lineEdit.setText('База удалена')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()



if __name__ == '__main__':
    main()