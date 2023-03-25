from functools import partial

import sqlalchemy
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from common_func import def_msg_box


def delete_rows(db_con, table, list_dict: list):
    if not list_dict:
        return

    for col_value_dict in list_dict:
        delete_query = sqlalchemy.delete(table)
        for col in col_value_dict:
            delete_query = delete_query.where(col == col_value_dict[col])
        cur = db_con.execute(delete_query)
        res = def_msg_box.DefMsgBox("Вы действительно хотите пролоджить?", "Подтверждение").result()
        if res == QMessageBox.Ok:
            db_con.commit()


def set_view_delete_row(view_table, columns):
    view_table.setColumnCount(len(columns))
    labels_columns = list()
    for column in columns:
        header_table_label = f"Столбец {column['name']} {column['type']}"
        labels_columns.append(header_table_label)

    view_table.setHorizontalHeaderLabels(labels_columns)
    view_table.resizeColumnsToContents()


def setup_settings_layout(settings_layout, db_con, view_table, sql_table):
    settings_layout.clear_layout()

    settings_label = QLabel("<b>Настройка для действия</b>")

    add_deletable_row_btn = QPushButton("Добавить запись на удаление")
    add_deletable_row_btn.clicked.connect(partial(view_table.insertRow, view_table.rowCount()))

    exclude_deletable_row_btn = QPushButton("Убрать запись из списка на удаление")
    exclude_deletable_row_btn.clicked.connect(partial(exclude_row, view_table))

    delete_rows_btn = QPushButton("Удалить вписанные записи")
    delete_rows_btn.clicked.connect(partial(execute_delete_query, db_con, view_table, sql_table))

    settings_layout.addWidget(settings_label)
    settings_layout.addWidget(add_deletable_row_btn)
    settings_layout.addWidget(exclude_deletable_row_btn)
    settings_layout.addWidget(delete_rows_btn)


def exclude_row(view_table):
    select = view_table.selectionModel()

    for deletable_row in select.selectedRows():
        view_table.removeRow(deletable_row.row())


def get_column_value_dict(view_table, sql_table):
    lst_col_value_dicts = list()

    for i in range(view_table.rowCount()):
        col_value_dict = dict()
        for j in range(view_table.columnCount()):
            cell = view_table.item(i, j)
            if cell:
                value = cell.text()
                sql_col = getattr(sql_table.c, view_table.horizontalHeaderItem(j).text().split(' ')[1])
                col_value_dict[sql_col] = value

        lst_col_value_dicts.append(col_value_dict)

    return lst_col_value_dicts


def execute_delete_query(db_con, view_table, sql_table):
    lst_col_value_dicts = get_column_value_dict(view_table, sql_table)
    delete_rows(db_con, sql_table, lst_col_value_dicts)
