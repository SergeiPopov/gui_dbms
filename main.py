import sys

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtPrintSupport import *

from Pages.entry_page import EntryPage


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('GUI_DBMS')
        self.setGeometry(100, 100, 1200, 600)
        start_page = EntryPage(self)
        self.setCentralWidget(start_page)
        self.show()

    def change_page(self, ptr_widget_page):
        self.setCentralWidget(ptr_widget_page)


if __name__ == '__main__':
    app = QApplication([])
    main_win = MainWindow()
    sys.exit(app.exec())