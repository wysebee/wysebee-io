
import sys
import os
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage

from Wysebee import Wysebee
from Wysebee import WysebeeBackend

from src.api import Api

class Backend(WysebeeBackend):
    def __init__(self, parent):
        super().__init__(parent)

    @Slot(result=list)
    def getTodoList(self):
        todo_list = Api().get_todos()
        return todo_list


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Wysebee")
    app.setApplicationName("Todo")
    app.setApplicationName("Todo")
    wysebee = Wysebee(app)
    backend = Backend(app)
    browser = wysebee.initialize_browser(width=1280, height=800, backend=backend)
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui/templates/index.html"))
    browser.load(QUrl.fromLocalFile(html_path))
    browser.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
