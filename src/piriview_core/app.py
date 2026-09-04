"""Main application window for PiriView Core."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
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

        self.status_label = QLabel("No study loaded")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.status_label)

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
            self.status_label.setText("No DICOM series found")
            return

        image_count = sum(
            len(datasets) for datasets in self.series.values()
        )

        self.status_label.setText(
            f"Loaded {len(self.series)} DICOM series\n"
            f"{image_count} images"
        )


def run():
    """Start the PiriView Core application."""

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())
