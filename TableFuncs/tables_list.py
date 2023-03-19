import sqlalchemy as sl

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


def get_tables_list(db_con, specified_schema=None):
    inspector = sl.inspect(db_con)
    tables = inspector.get_table_names(schema=specified_schema)
    return tables


def set_view_tables_list(view_table, tables: list):
    view_table.setRowCount(len(tables))
    view_table.setColumnCount(1)
    view_table.setHorizontalHeaderLabels(["Название таблицы"])

    for i, table in enumerate(tables):
        view_table.setItem(i, 0, QTableWidgetItem(table))

    view_table.resizeColumnsToContents()
