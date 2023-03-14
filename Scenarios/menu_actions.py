from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy as sl

from .def_msg_box import DefMsgBox
from .table_page import TablePage


class MenuPage(QWidget):
    def __init__(self, db_con, parent=None):
        super(MenuPage, self).__init__(parent)

        self.db_con = db_con
        self.inspector = sl.inspect(self.db_con)
        self.metadata = sl.MetaData()

        self.table_page_btn = QPushButton("Работа с таблицами")
        self.get_rows_btn = QPushButton("Получить список записей")
        self.create_table_btn = QPushButton("Создать таблицу")


        actions_layout = QVBoxLayout(self)

        actions_layout.addWidget(self.table_page_btn)


        self.table_page_btn.clicked.connect(self.set_table_page)


    def get_schemas(self):
        schemas = self.inspector.get_schema_names()
        self.view_table.setRowCount(len(schemas))
        self.view_table.setColumnCount(1)
        self.view_table.setHorizontalHeaderItem(0, QTableWidgetItem("Схемы базы данных"))
        self.view_table.horizontalHeader().setStretchLastSection(True)
        for i, schema in enumerate(schemas):
            self.view_table.setItem(i, 0, QTableWidgetItem(schema))

    def get_table_list(self):
        tables = self.inspector.get_table_names(schema=self.specified_schema.text())
        self.view_table.setRowCount(len(tables))
        self.view_table.setColumnCount(1)
        self.view_table.setHorizontalHeaderItem(0, QTableWidgetItem(f"Таблицы схемы {self.specified_schema.text()}"))
        self.view_table.horizontalHeader().setStretchLastSection(True)
        for i, table in enumerate(tables):
            self.view_table.setItem(i, 0, QTableWidgetItem(table))

    def set_table_page(self):
        main_window = self.parent()
        main_window.change_page(TablePage(self.db_con, main_window))



