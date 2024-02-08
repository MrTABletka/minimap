import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QPixmap

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Main_menu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 500)
        self.setFixedSize(self.geometry().width(), self.geometry().height())
        self.setWindowTitle('Minimap')

        map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
        response = requests.get(map_request)

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
        self.labl.setGeometry(0, 0, 900, 500)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    window_menu = Main_menu()


    window_menu.show()
    sys.exit(app.exec_())
