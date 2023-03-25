from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy


def get_table_info(db_con, table_name, schema=None):
    inspector = sqlalchemy.inspect(db_con)
    columns = inspector.get_columns(table_name, schema=schema)
    if not len(columns):
        return

    return columns


def set_view_table_columns_info(view_table, columns):
    max_row, i = max([(len(row), i) for i, row in enumerate(columns)])

    view_table.setRowCount(len(columns))
    view_table.setColumnCount(max_row)
    view_table.setHorizontalHeaderLabels(columns[i].keys())

    for i, col in enumerate(columns):
        for j, info in enumerate(col):
            view_table.setItem(i, j, QTableWidgetItem(col.get(info).__repr__()))


def get_table(db_con, table_name, schema=None):
    schema = schema if not schema else None
    meta = sqlalchemy.MetaData(schema=schema)
    table = sqlalchemy.Table(table_name, meta, autoload_with=db_con.engine)
    return table