import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QFont, QPixmap
import time
import keyboard

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def Check_key():
    while True:
        keyboard.wait("a")
        print("You pressed 'a'.")

def Request(x, y, size, type):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={size},0.002&l={type}"
    return requests.get(map_request)

def Poisk_po_organiachiiam(size, name):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"}

    return requests.get(geocoder_api_server, params=geocoder_params)



class Main_menu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 600)
        self.setFixedSize(self.geometry().width(), self.geometry().height())
        self.setWindowTitle('Minimap')

        response = Request(37.530887, 55.703110, 0.002, 'map')
        self.x = 37.530887
        self.y =  55.703110
        self.size = 0.002
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.picture = QPixmap('map.png')
        self.labl = QLabel(self)
        self.labl.setPixmap(self.picture)
        self.labl.setGeometry(0, 0, 600, 450)

        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(250, 475, 150, 50)

        search_btn = QPushButton('Искать', self)
        search_btn.setGeometry(250, 525, 150, 50)
        search_btn.setFont(QFont('Times', 14))
        search_btn.clicked.connect(self.search)

        move_up_btn = QPushButton('UP', self)
        move_up_btn.setGeometry(75, 475, 50, 50)
        move_up_btn.setFont(QFont('Times', 7))
        move_up_btn.clicked.connect(self.up)

        move_down_btn = QPushButton('DOWN', self)
        move_down_btn.setGeometry(75, 525, 50, 50)
        move_down_btn.setFont(QFont('Times', 7))
        move_down_btn.clicked.connect(self.down)


        move_right_btn = QPushButton('>', self)
        move_right_btn.setGeometry(125, 525, 50, 50)
        move_right_btn.setFont(QFont('Times', 15))
        move_right_btn.clicked.connect(self.right)


        move_left_btn = QPushButton('<', self)
        move_left_btn.setGeometry(25, 525, 50, 50)
        move_left_btn.setFont(QFont('Times', 15))
        move_left_btn.clicked.connect(self.left)


    def closeEvent(self, event):
        # Убираем файл
        os.remove(self.map_file)

    def up(self):
        self.y += self.size * 1.5
        response = Request(self.x, self.y, self.size, 'map')
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.picture = QPixmap('map.png')
        self.labl.setPixmap(self.picture)

    def down(self):
        self.y -= self.size * 1.5
        response = Request(self.x, self.y, self.size, 'map')
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.picture = QPixmap('map.png')
        self.labl.setPixmap(self.picture)

    def left(self):
        self.x -= self.size * 3
        response = Request(self.x, self.y, self.size, 'map')
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.picture = QPixmap('map.png')
        self.labl.setPixmap(self.picture)

    def right(self):
        self.x += self.size * 3
        response = Request(self.x, self.y, self.size, 'map')
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.picture = QPixmap('map.png')
        self.labl.setPixmap(self.picture)

    def search(self):
        toponyms = Poisk_po_organiachiiam(self.size, self.line_edit.text()).json()
        self.x, self.y = toponyms["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
        response = Request(self.x, self.y, self.size, 'map')
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.picture = QPixmap('map.png')
        self.labl.setPixmap(self.picture)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_menu = Main_menu()

    window_menu.show()
    sys.exit(app.exec_())
