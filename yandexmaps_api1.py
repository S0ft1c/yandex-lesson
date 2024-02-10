import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests


class MapApp(QWidget):
    def __init__(self, api_key, latitude, longitude, zoom):
        super().__init__()

        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Yandex Map App')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

        self.showMap()

    def showMap(self):
        url = f'https://api-maps.yandex.ru/2.1/?apikey={self.api_key}&lang=en_US'
        html = f'<html><head><script src="{url}" type="text/javascript"></script></head>' \
               f'<body><div id="map" style="width: 100%; height: 100%;"></div>' \
               f'<script type="text/javascript">' \
               f'ymaps.ready(init); ' \
               f'function init(){{var myMap = new ymaps.Map("map", {{center: [{self.latitude}, {self.longitude}], zoom: {self.zoom}}});}}</script>' \
               f'</body></html>'

        self.webview.setHtml(html)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python main.py <api_key> <latitude> <longitude> <zoom>")
        sys.exit(1)

    app = QApplication(sys.argv)
    api_key, latitude, longitude, zoom = sys.argv[1:]
    map_app = MapApp(api_key, float(latitude), float(longitude), int(zoom))
    map_app.show()
    sys.exit(app.exec_())
