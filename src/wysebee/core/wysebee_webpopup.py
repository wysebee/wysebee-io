from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit

class WysebeeWebPopup(QWidget):
    def __init__(self, url: str, title: str, show_url_bar: bool = False):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(800, 800)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if show_url_bar:
            self.url_bar = QLineEdit()
            self.url_bar.setText(url)
            self.url_bar.setReadOnly(True)
            layout.addWidget(self.url_bar)

        self.web_view = QWebEngineView()
        self.web_view.load(QUrl(url))

        layout.addWidget(self.web_view)
