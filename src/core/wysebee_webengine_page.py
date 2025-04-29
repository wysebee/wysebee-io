import logging
from PySide6.QtWebEngineCore import QWebEnginePage

logger = logging.getLogger("wysebee")

class WysebeeWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        logger.info(f"[JS] {message}")

    def urlChanged(self, url):
        logger.info(f"URL changed to: {url}")
