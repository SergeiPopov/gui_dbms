from functools import partial

import sqlalchemy
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from TableFuncs import table_info
from common_func.def_msg_box import DefMsgBox


def create_rows_and_commit(db_con, sql_table, list_new_rows):
    try:
        for row in list_new_rows:
            if not len(row):
                continue
            create_query = sqlalchemy.insert(sql_table).values(row)
            db_con.execute(create_query)
            db_con.commit()
    except:
        DefMsgBox("Ошибка создания", "Что то пошло не так при добавлении записей")


def set_view_create_rows(page):
    view_table = page.findChildren(QTableWidget, "view_table")[0]
    table_name = page.findChildren(QLineEdit, "table_name_line_edit")[0].text()
    schema_name = page.findChildren(QLineEdit, "schema_name_line_edit")[0].text()
    schema_name = None if schema_name == "" else schema_name

    column_labels, sql_columns_info = table_info.get_column_labels(page.db_con, table_name, schema_name)

    view_table.clear()
    view_table.setRowCount(1)
    view_table.setColumnCount(len(sql_columns_info))
    view_table.setHorizontalHeaderLabels(column_labels)


def setup_settings_layout(page):
    view_table = page.findChildren(QTableWidget, "view_table")[0]
    table_name = page.findChildren(QLineEdit, "table_name_line_edit")[0].text()
    schema_name = page.findChildren(QLineEdit, "schema_name_line_edit")[0].text()
    schema_name = schema_name if schema_name else ""

    settings_layout = page.settings_action_layout
    settings_layout.clear_layout()

    settings_label = QLabel("<b>Настройка для действия СОЗДАНИЕ</b>")
    table_name_label = QLabel(f"Настройки записей для {schema_name} {table_name}", page)
    table_name_label.setObjectName("settings_label_with_schema_and_table")

    add_new_view_row_btn = QPushButton("Добавить ещё одну строку на создание")
    add_new_view_row_btn.clicked.connect(partial(view_table.insertRow, view_table.rowCount()))

    accept_new_view_rows_btn = QPushButton("Добавить ещё одну строку на создание")
    accept_new_view_rows_btn.clicked.connect(partial(clicked_create_rows_btn, page))

    settings_layout.addWidget(settings_label)
    settings_layout.addWidget(table_name_label)
    settings_layout.addWidget(add_new_view_row_btn)
    settings_layout.addWidget(accept_new_view_rows_btn)


def get_new_rows_dict(page):
    view_table = page.findChildren(QTableWidget, "view_table")[0]
    settings_label = page.findChildren(QLabel, "settings_label_with_schema_and_table")[0].text()
    table_name = settings_label.split(" ")[-1]
    schema_name = settings_label.split(" ")[-2]
    schema_name = schema_name if schema_name else None
    sql_table = table_info.get_table(page.db_con, table_name, schema_name)
    list_new_rows = list()
    for i in range(view_table.rowCount()):
        col_and_value = dict()
        for j in range(view_table.columnCount()):
            cell = view_table.item(i, j)
            if cell:
                value = cell.text()
                col_name = view_table.horizontalHeaderItem(j).text().split(" ")[0]
                col_and_value[col_name] = value
        list_new_rows.append(col_and_value)

    return list_new_rows, sql_table


def clicked_create_rows_btn(page):
    list_new_rows, sql_table = get_new_rows_dict(page)
    res = DefMsgBox("Подтверждение создания строк", "Вы действительно хотите добавить новые записи?").result()
    if res == QMessageBox.Ok:
        create_rows_and_commit(page.db_con, sql_table, list_new_rows)