import logging
from PySide6.QtCore import QObject, Slot
from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtNetwork import QHostAddress, QSslSocket
from PySide6.QtWebChannel import QWebChannel
from .resource_loader import ResourceLoader
from .wysebee_webview import WysebeeWebView
from .wysebee_webengine_page import WysebeeWebEnginePage
from .wysebee_backend import WysebeeBackend
from .websocket_client_wrapper import WebSocketClientWrapper

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
class Wysebee(QObject):
    def __init__(self, app):
      super().__init__()
      self._app = app
      self._wsserver = QWebSocketServer(
          "QWebChannel Standalone Example Server",
          QWebSocketServer.SslMode.NonSecureMode,
      )
      if not self._wsserver.listen(QHostAddress.SpecialAddress.LocalHost, 12345):
          logger.error("Failed to open web socket server.")
          raise RuntimeError("Failed to open web socket server.")
      self._resource_loader = ResourceLoader()
      self._resource_loader.init_handler()
      self._browser = WysebeeWebView()
      self._browser.loadFinished.connect(self.pageLoaded)
      self._browser.setPage(WysebeeWebEnginePage(self._browser))
      self._channel = QWebChannel(self._browser)
      self._backend = None

    def initialize_browser(self, width = None, height = None, backend = None):
        if backend is None:
            backend = WysebeeBackend(self._app)
        self._backend = backend
        self._browser.dropFile.connect(backend.onDropFile)
        self._channel.registerObject("wysebee", backend)

        client_wrapper = WebSocketClientWrapper(self._wsserver)
        client_wrapper.client_connected.connect(self._channel.connectTo)

        self._browser.page().setWebChannel(self._channel)
        self._client_wrapper = client_wrapper
        if width is not None and height is not None:
          self._browser.resize(width, height)
        return self._browser

    @Slot(bool)
    def pageLoaded(self, result):
      self._backend.onInitialized(result)