import sys
from io import BytesIO

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtWidgets import QLineEdit, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QKeySequence
from PyQt6.QtCore import Qt

import requests
from PIL import Image


class Maps(QMainWindow):
    def __init__(self):
        super().__init__()
        self.longitude = '38'
        self.latitude = '56'
        self.delta = '0.01'  # Масштаб
        self.move_k = float(self.delta) / 4  # Насколько градусов передвигается карта
        self.apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 600, 700)
        self.setWindowTitle('Карты')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QLabel(self)
        self.map = QPixmap('map.png')

        self.refresh_map()

        self.label.setPixmap(self.map)
        self.label.adjustSize()

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.label)
        self.central_widget.setLayout(layout)  # Установка Layout для central_widget

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def refresh_map(self):
        map_params = {
            "ll": ",".join([self.longitude, self.latitude]),
            "spn": ",".join([self.delta, self.delta]),
            "apikey": self.apikey,
            "l": "map"  # Ensure the map layer is specified
        }

        map_api_server = "https://static-maps.yandex.ru/v1"
        try:
            response = requests.get(map_api_server, params=map_params, timeout=5)  # Add timeout
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            im = BytesIO(response.content)
            opened_image = Image.open(im)
            opened_image.save('map.png')
            self.map = QPixmap('map.png')
            self.label.setPixmap(self.map)
            self.label.update()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            # Handle the error (e.g., display a default image or error message)
            self.label.setText("Ошибка загрузки карты.")

    def keyPressEvent(self, event):
        key = event.key()
        max_latitude = 85.0511
        min_latitude = -85.0511
        max_longitude = 179.9999
        min_longitude = -179.9999
        min_delta = 0.0001
        max_delta = 50
        zoom_step = 0.005
        if key == Qt.Key.Key_Up:
            new_latitude = self.move_k + float(self.latitude)
            if new_latitude <= max_latitude:
                self.latitude = str(new_latitude)
        elif key == Qt.Key.Key_Down:
            new_latitude = float(self.latitude) - self.move_k
            if new_latitude >= min_latitude:
                self.latitude = str(new_latitude)
        elif key == Qt.Key.Key_Left:
            new_longitude = float(self.longitude) - self.move_k
            if new_longitude >= min_longitude:
                self.longitude = str(new_longitude)
        elif key == Qt.Key.Key_Right:
            new_longitude = self.move_k + float(self.longitude)
            if new_longitude <= max_longitude:
                self.longitude = str(new_longitude)
        elif key == Qt.Key.Key_W: #Увеличение мастштаба
            new_delta = float(self.delta) - zoom_step
            if new_delta >= min_delta:
                self.delta = str(new_delta)
                self.move_k = float(self.delta) / 4
        elif key == Qt.Key.Key_S: #Уменьшение мастштаба
            new_delta = float(self.delta) + zoom_step
            if new_delta <= max_delta:
                self.delta = str(new_delta)
                self.move_k = float(self.delta) / 4

        self.refresh_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Maps()
    ex.show()
    sys.exit(app.exec())