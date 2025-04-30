# Compilation mode, support OS-specific options
# nuitka-project-if: {OS} in ("Windows", "Linux", "Darwin", "FreeBSD"):
#    nuitka-project: --output-dir=dist
# nuitka-project-else:
#    nuitka-project: --mode=standalonealone

# The PySide6 plugin covers qt-plugins
# nuitka-project: --macos-create-app-bundle
# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --include-qt-plugins=qml
# nuitka-project: --include-data-file=view.qml=view.qml
# nuitka-project: --include-data-dir=templates=templates

import sys
import os
import json
import base64
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtGui import QDropEvent
from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

def setup_logging():
    logger = logging.getLogger('wysebee')
    logger.setLevel(logging.DEBUG)

    # Console handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)

    # File handler
    f_handler = logging.FileHandler('gallery.log')
    f_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    # Add handlers (only if not already added)
    if not logger.handlers:
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

setup_logging()

from Wysebee import Wysebee
from Wysebee import WysebeeBackend
class Backend(WysebeeBackend):
    def __init__(self, parent):
        super().__init__(parent)

    @Slot(result=list)
    def getImages(self):
        return ["images/1.jpg", "images/2.jpg", "images/3.jpg", "images/4.jpg", "images/5.jpg", "images/6.jpg"]

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Wysebee")
    app.setApplicationName("Gallery")
    app.setApplicationName("Gallery")
    wysebee = Wysebee(app)
    backend = Backend(app)
    browser = wysebee.initialize_browser(width=1280, height=800, backend=backend)
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui/templates/index.html"))

    '''
    devtools_view = QWebEngineView()
    browser.page().setDevToolsPage(devtools_view.page())

    # Open DevTools window
    devtools_view.resize(800, 600)
    devtools_view.show()  # Comment this out if you want to open DevTools later
    '''

    browser.load(QUrl.fromLocalFile(html_path))
    browser.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()