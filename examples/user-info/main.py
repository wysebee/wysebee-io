
import sys
import os
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from Wysebee import Wysebee
from Wysebee import WysebeeBackend

from src.database import get_user_info, run_migrations, save_user_info

class Backend(WysebeeBackend):

    def __init__(self, parent):
        super().__init__(parent)

    @Slot(str, result=dict)
    def getUserInfo(self, userId):
        print(f"📩 Received userId: {userId}")
        user_info = get_user_info(userId)
        return { "name": user_info.name,
                 "email": user_info.email,
                 "avatar": user_info.avatar,
                }
def main():
    run_migrations()
    user_info = {
        "userId": "1234567890",
        "name": "Jeff", 
        "email": "jeff@test.com",
        "avatar": "data/default.jpg",
    }
    save_user_info(user_info)
    app = QApplication(sys.argv)
    wysebee = Wysebee(app)
    backend = Backend(app)
    browser = wysebee.initialize_browser(width=1280, height=800, backend=backend)
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui/templates/index.html"))
    browser.load(QUrl.fromLocalFile(html_path))
    browser.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
