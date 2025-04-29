from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QDropEvent
from PySide6.QtCore import Signal

class WysebeeWebView(QWebEngineView):
    dropFile = Signal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path:
                self.dropFile.emit(path)
