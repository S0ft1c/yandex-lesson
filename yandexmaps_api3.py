import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt


class MapApp(QWidget):
    def __init__(self, api_key, initial_latitude, initial_longitude, initial_zoom):
        super().__init__()

        self.api_key = api_key
        self.latitude = initial_latitude
        self.longitude = initial_longitude
        self.zoom = initial_zoom

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
               f'function init(){{var myMap = new ymaps.Map("map", {{center: [{self.latitude}, {self.longitude}], zoom: {self.zoom}}}); ' \
               f'window.myMap = myMap;}}</script>' \
               f'</body></html>'

        self.webview.setHtml(html)
        self.webview.page().loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self):
        # Подключаем обработчики клавиш после полной загрузки карты
        self.webview.page().runJavaScript(
            'document.addEventListener("keydown", function(event) { window.pywebview.api.keyPressEvent(event); });')

    def keyPressEvent(self, event):
        step_size = 0.1  # Размер шага для перемещения центра карты
        speed_factor = self.zoom / 1000  # Коэффициент скорости от зума

        if event.key() == Qt.Key_PageUp:
            self.zoomIn()
        elif event.key() == Qt.Key_PageDown:
            self.zoomOut()
        elif event.key() == Qt.Key_Left:
            self.moveMap(0, -step_size / speed_factor)
        elif event.key() == Qt.Key_Right:
            self.moveMap(0, step_size / speed_factor)
        elif event.key() == Qt.Key_Down:
            self.moveMap(-step_size / speed_factor, 0)
        elif event.key() == Qt.Key_Up:
            self.moveMap(step_size / speed_factor, 0)

    def zoomIn(self):
        if self.zoom < 20:
            self.zoom += 1
            self.updateMap()

    def zoomOut(self):
        if self.zoom > 1:
            self.zoom -= 1
            self.updateMap()

    def moveMap(self, delta_latitude, delta_longitude):
        # Перемещение центра карты на указанные значения
        new_latitude = self.latitude + delta_latitude
        new_longitude = self.longitude + delta_longitude

        # Проверка предельных значений координат
        if -90 <= new_latitude <= 90 and -180 <= new_longitude <= 180:
            self.latitude = new_latitude
            self.longitude = new_longitude
            self.updateMap()

    def updateMap(self):
        # Обновляем карту при изменении масштаба или центра
        self.webview.page().runJavaScript(f"myMap.setZoom({self.zoom});")
        self.webview.page().runJavaScript(f"myMap.setCenter([{self.latitude}, {self.longitude}]);")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python main.py <api_key> <initial_latitude> <initial_longitude> <initial_zoom>")
        sys.exit(1)

    app = QApplication(sys.argv)
    api_key, initial_latitude, initial_longitude, initial_zoom = sys.argv[1:]
    map_app = MapApp(api_key, float(initial_latitude), float(initial_longitude), int(initial_zoom))
    map_app.show()
    sys.exit(app.exec_())
