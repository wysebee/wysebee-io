import mimetypes
import os
import logging
from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6 import QtCore, QtWebEngineCore, QtWebEngineWidgets
from PySide6.QtWebEngineCore import QWebEngineUrlSchemeHandler, QWebEngineUrlRequestJob, QWebEngineUrlScheme

logger = logging.getLogger("wysebee")
class ResourceSchemeHandler(QtWebEngineCore.QWebEngineUrlSchemeHandler):
    def __init__(self, app):
        super().__init__(app)
        self.m_app = app
        self._buffers = {}

    def requestStarted(self, job: QWebEngineUrlRequestJob):
        url = job.requestUrl()
        path = url.path()  # e.g., /upload/myfile.txt
        url_str = url.toString()

        if url_str.startswith("wysebee://openfile/"):
            file_path = url_str[len("wysebee://openfile/?file="):]
            if not os.path.isfile(file_path):
                logger.error("❌ File not found:", file_path)
                job.fail(QWebEngineUrlRequestJob.UrlNotFound)
                return
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = "application/octet-stream"
            logger.info(f"Detected MIME type: {mime_type}")
            mime_type = mime_type.encode("utf-8")
            with open(file_path, "rb") as f:
                data = f.read()
            logger.info(f"File size: {len(data)} bytes")
            buffer = QBuffer()
            buffer.setData(QByteArray(data))
            buffer.open(QIODevice.ReadOnly)
            logger.info(f"Buffer size: {buffer.size()} bytes")
            # 🔁 Keep buffer alive by attaching it to the job or handler
            job._buffer = buffer
            self._buffers[id(job)] = buffer
            job.destroyed.connect(lambda: self._buffers.pop(id(job), None))
            logger.info(f"📦 Sending file ({len(data)} bytes), MIME: {mime_type}")
            job.reply(mime_type, buffer)
        else:
            # Respond with 404 or fallback
            job.fail(QWebEngineUrlRequestJob.UrlInvalid)

class ResourceLoader(QtCore.QObject):
    scheme = b"wysebee"

    def __init__(self, parent=None):
        super().__init__(parent)
        scheme = QtWebEngineCore.QWebEngineUrlScheme(ResourceLoader.scheme)
        scheme.setFlags(
            QWebEngineUrlScheme.SecureScheme |
            QWebEngineUrlScheme.LocalScheme |
            QWebEngineUrlScheme.LocalAccessAllowed |
            QtWebEngineCore.QWebEngineUrlScheme.CorsEnabled
        )
        QtWebEngineCore.QWebEngineUrlScheme.registerScheme(scheme)
        self.m_functions = dict()

    def init_handler(self, profile=None):
        if profile is None:
            profile = QtWebEngineCore.QWebEngineProfile.defaultProfile()
        handler = profile.urlSchemeHandler(ResourceLoader.scheme)
        if handler is not None:
            profile.removeUrlSchemeHandler(handler)

        self.m_handler = ResourceSchemeHandler(self)
        profile.installUrlSchemeHandler(ResourceLoader.scheme, self.m_handler)

    def register(self, name):
        def decorator(f):
            self.m_functions[name] = f
            return f

        return decorator

    def create_url(self, name):
        url = QtCore.QUrl()
        url.setScheme(ResourceLoader.scheme.decode())
        url.setHost(name)
        return url