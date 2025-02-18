import sys
from io import BytesIO

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import QLineEdit, QLabel
from PyQt6.QtGui import QPixmap

import requests
from PIL import Image



class Maps(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle('Карты')

        # Координаты
        self.longitude = '38'
        self.latitude = '56'

        # Масштаб
        self.delta = "0.1"

        # Ключ к API
        self.apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

        # Обновляем картинку
        self.refresh_map()

        self.map = QPixmap('map.png')
        self.label = QLabel(self)
        self.label.setPixmap(self.map)
        self.label.adjustSize()


    def refresh_map(self):
        map_params = {
            "ll": ",".join([self.longitude, self.latitude]),
            "spn": ",".join([self.delta, self.delta]),
            "apikey": self.apikey,

        }

        map_api_server = "https://static-maps.yandex.ru/v1"
        response = requests.get(map_api_server, params=map_params)
        im = BytesIO(response.content)
        opened_image = Image.open(im)
        opened_image.save('map.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Maps()
    ex.show()
    sys.exit(app.exec())
