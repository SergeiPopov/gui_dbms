import sqlalchemy
from PySide6.QtWidgets import *

from Layouts.Layout import Layout
from common_func.def_msg_box import DefMsgBox
from Pages.table_page import TableInfoPage
class EntryPage(QWidget):
    def __init__(self, parent=None):
        super(EntryPage, self).__init__(parent)

        # Слой для основных функциональных кнопок
        self.functional_layout = Layout(QBoxLayout.Direction.TopToBottom, parent)

        # Основные функциональные кнопки
        self.connect_line_edit = QLineEdit("Введите URL подключения. Например sqlite:///lib.db")
        self.connect_btn = QPushButton("Подключиться")
        self.connect_btn.clicked.connect(self.test_connection)

        self.functional_layout.addWidget(self.connect_line_edit)
        self.functional_layout.addWidget(self.connect_btn)

        # Отображение функционального слоя на странице
        self.setLayout(self.functional_layout)

    def test_connection(self):
        try:
            con_url = self.connect_line_edit.text()
            db_con = sqlalchemy.create_engine(con_url).connect()
            table_page = TableInfoPage(db_con, self.parent())
            self.parent().change_page(table_page)
        except:
            DefMsgBox("Ошибка подключения", "Не удалось подключится к БД")
