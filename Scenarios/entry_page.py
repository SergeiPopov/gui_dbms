from PySide6.QtWidgets import *

import sqlalchemy as sl

from common_func.def_msg_box import DefMsgBox
from .menu_actions import MenuPage


class EntryPage(QWidget):
    def __init__(self, parent=None):
        super(EntryPage, self).__init__(parent)

        self.conn_edit_line = QLineEdit("mssql+pyodbc://SA:libdev2023@127.0.0.1:1433/books_19?driver=ODBC+Driver+17+for+SQL+Server&encrypt=no", self)
        self.conn_but = QPushButton("Подключиться")

        layout = QVBoxLayout(self)
        layout.addWidget(self.conn_edit_line)
        layout.addWidget(self.conn_but)

        self.conn_but.clicked.connect(self.try_connect)

    def try_connect(self):
        try:
            conn_url = self.conn_edit_line.text()
            self.engine = sl.create_engine(conn_url, echo=False)
            self.db_con = self.engine.connect()
            DefMsgBox("Успешное подключение", "Подключение выполнено")

            main_window = self.parent()
            mp = MenuPage(self.db_con, parent=main_window)
            main_window.change_page(mp)
        except:
            DefMsgBox("Ошибка подключения", "Проверьте URL")

    def get_db_conn(self):
        return self.db_con