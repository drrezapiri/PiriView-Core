"""Main application window for PiriView Core."""

import sys

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
)

from piriview_core.dicom_loader import load_dicom_series


class MainWindow(QMainWindow):
    """Main PiriView Core application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PiriView Core")
        self.resize(1000, 700)

        self.series = {}

        self.image_label = QLabel("No study loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: black; color: white;")
        self.setCentralWidget(self.image_label)

        self._create_menu()

    def _create_menu(self):
        """Create the application menu."""

        file_menu = self.menuBar().addMenu("&File")

        open_folder_action = QAction("Open Folder...", self)
        open_folder_action.setShortcut("Ctrl+O")
        open_folder_action.triggered.connect(self.open_folder)

        file_menu.addAction(open_folder_action)

    def open_folder(self):
        """Select a folder and load the DICOM series it contains."""

        folder = QFileDialog.getExistingDirectory(
            self,
            "Open DICOM Folder",
        )

        if not folder:
            return

        try:
            self.series = load_dicom_series(folder)
        except (OSError, ValueError) as error:
            QMessageBox.critical(
                self,
                "Unable to open folder",
                str(error),
            )
            return

        if not self.series:
            self.image_label.setText("No DICOM series found")
            return

        first_series = next(iter(self.series.values()))

        if not first_series:
            self.image_label.setText("No images found")
            return

        try:
            self.display_dataset(first_series[0])
        except Exception as error:
            QMessageBox.critical(
                self,
                "Unable to display image",
                str(error),
            )

    def display_dataset(self, dataset):
        """Display one DICOM dataset as a grayscale image."""

        pixel_array = dataset.pixel_array.astype(np.float32)

        minimum = float(pixel_array.min())
        maximum = float(pixel_array.max())

        if maximum > minimum:
            pixel_array = (
                (pixel_array - minimum)
                / (maximum - minimum)
                * 255.0
            )
        else:
            pixel_array = np.zeros_like(pixel_array)

        pixel_array = pixel_array.astype(np.uint8)

        if getattr(dataset, "PhotometricInterpretation", "") == "MONOCHROME1":
            pixel_array = 255 - pixel_array

        height, width = pixel_array.shape

        image = QImage(
            pixel_array.data,
            width,
            height,
            pixel_array.strides[0],
            QImage.Format.Format_Grayscale8,
        ).copy()

        pixmap = QPixmap.fromImage(image)

        pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.image_label.setText("")
        self.image_label.setPixmap(pixmap)


def run():
    """Start the PiriView Core application."""

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())
