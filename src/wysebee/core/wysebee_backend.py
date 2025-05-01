import os
import json
import logging
from PySide6.QtCore import QObject, Slot, Signal

logger = logging.getLogger("wysebee")

class WysebeeBackend(QObject):

    sendFile = Signal(str, int)

    def __init__(self, parent):
        super().__init__(parent)

    @Slot(str, result=str)
    def sendMessage(self, message):
        logger.info(f"📩 Received message: {message}")
        return json.dumps("roger")

    @Slot(str, int)
    def onDropFile(self, file_path):
        logger.info(f"📥 pass file path to ui: {file_path}")
        self.sendFile.emit(file_path, os.path.getsize(file_path))

    def onInitialized(self, result):
        """
        This method should be implemented by child classes to handle initialization.
        
        Args:
            result: The result of the initialization process
        """
        pass