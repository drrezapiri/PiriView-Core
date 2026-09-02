"""Main application window for PiriView Core."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    """Main PiriView Core application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PiriView Core")
        self.resize(1000, 700)

        placeholder = QLabel("No study loaded")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(placeholder)


def run():
    """Start the PiriView Core application."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())
