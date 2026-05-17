# Nama  : Dodi Wijaya
# NIM   : F1D02310047
# Kelas : Pemrograman Visual D

import sys
import os

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    style_path = os.path.join(
        BASE_DIR,
        "styles",
        "style.qss"
    )

    if os.path.exists(style_path):

        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())

    window = MainWindow()

    window.show()

    sys.exit(app.exec())