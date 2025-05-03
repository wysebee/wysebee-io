
import sys
import os
import cv2
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from Wysebee import Wysebee
from Wysebee import WysebeeBackend
from Wysebee.core.temp_helper import TempFileHelper

class Backend(WysebeeBackend):

    def __init__(self, parent):
        super().__init__(parent)

    @Slot()
    def openFileDialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if dialog.exec():
            selected_files = dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                print(f"📁 User selected: {file_path}")
                self.sendFile.emit(file_path, os.path.getsize(file_path))

    @Slot(str, result=str)
    def process_image(self, image_path):
        print(f"📷 Processing image: {image_path}")
        image = cv2.imread(image_path)
        print(f"Image shape: {image.shape}")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        TempFileHelper().create_temp_directory("output_gray.jpg")
        file_path = TempFileHelper().get_temp_file_path("output_gray.jpg")
        print("Saving processed image to:", file_path)
        cv2.imwrite(file_path, gray)
        return file_path

def main():
    TempFileHelper().create_base_directory("image-processor")
    app = QApplication(sys.argv)
    wysebee = Wysebee(app)
    backend = Backend(app)
    wysebee.initialize_window(width=1280, height=800, backend=backend)
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui/templates/index.html"))
    wysebee.launch(html_path)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
