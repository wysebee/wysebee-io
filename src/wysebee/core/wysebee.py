import logging
import os
import subprocess
from PySide6.QtCore import QObject, QUrl, QCoreApplication, QTimer, Signal
from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtNetwork import QHostAddress, QSslSocket
from PySide6.QtWebChannel import QWebChannel
from .resource_loader import ResourceLoader
from .wysebee_webview import WysebeeWebView
from .wysebee_webengine_page import WysebeeWebEnginePage
from .wysebee_backend import WysebeeBackend
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def setup_logging():
    logger = logging.getLogger('wysebee')
    logger.setLevel(logging.DEBUG)

    # Console handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)

    # File handler
    f_handler = logging.FileHandler('wysebee.log')
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

logger = logging.getLogger("wysebee")

class ReloadHandler(FileSystemEventHandler, QObject):
    reload = Signal()
    def __init__(self, parent):
      super().__init__(parent)

    def on_modified(self, event):
      self.reload.emit()

    def on_created(self, event):
      self.reload.emit()

    def on_deleted(self, event):
      self.reload.emit()

class Wysebee(QObject):
    def __init__(self, app):
      super().__init__()
      self._app = app
      self._isDev = False
      args = QCoreApplication.arguments()
      if len(args) > 1 and "--dev" in args:
          logger.debug("Running in development mode.")
          self._isDev = True
      self._resource_loader = ResourceLoader()
      self._resource_loader.init_handler()
      self._browser = WysebeeWebView()
      self._browser.setPage(WysebeeWebEnginePage(self._browser))
      self._channel = QWebChannel(self._browser)
      self._backend = None

    def initialize_window(self, width = None, height = None, backend = None):
        if backend is None:
            backend = WysebeeBackend(self._app)
        self._backend = backend
        self._browser.dropFile.connect(backend.onDropFile)
        self._channel.registerObject("wysebee", backend)

        self._browser.page().setWebChannel(self._channel)
        if width is not None and height is not None:
          self._browser.resize(width, height)
        return self._browser

    def launch(self, url: str):
      self._browser.load(QUrl.fromLocalFile(url))
      self._original_dir = os.getcwd()
      if self._isDev:
        self._html_dir = os.path.dirname(url)
        self._ui_dir = os.path.dirname(self._html_dir)
        self._source_dir = os.path.join(self._ui_dir, "src")

        # Watchdog observer
        self._ui_src_event_handler = ReloadHandler(self)
        self._ui_src_event_handler.reload.connect(self.schedule_rebuild_ui)
        self._ui_src_observer = Observer()
        self._ui_src_observer.schedule(self._ui_src_event_handler, self._source_dir, recursive=True)
        self._ui_src_observer.start()

        # Watchdog observer
        self._ui_event_handler = ReloadHandler(self)
        self._ui_event_handler.reload.connect(self.schedule_reload)
        self._ui_observer = Observer()
        self._ui_observer.schedule(self._ui_event_handler, self._html_dir, recursive=True)
        self._ui_observer.start()
      self._browser.show()

    def schedule_rebuild_ui(self):
        logger.info("Rebuilding ui ...")
        os.chdir(self._ui_dir)
        subprocess.Popen(
            ["npx", "vite", "build"],
        )

    def schedule_reload(self):
        logger.info("Reload ui ...")
        QTimer.singleShot(300, self._browser.reload)

    def closeEvent(self, event):
      logger.debug("Closing Wysebee application.")
      self.observer.stop()
      self.observer.join()
      event.accept()

    def browser(self):
      return self._browser
