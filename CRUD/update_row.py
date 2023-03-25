from functools import partial

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy as sl

def sql_query_update(db_con, sql_table, new_value, filter_value):
    pass


def set_view_update_row(page, columns_names, filter_value):
    view_table = page.findChildren(QTableWidget, "view_table")[0]
    view_table.clear()
    view_table.setRowCount(2)
    view_table.setColumnCount(len(columns_names))
    view_table.setHorizontalHeaderLabels(columns_names)
    view_table.setVerticalHeaderLabels(["Фильтр пред. записи", "Обновленные записи"])

    for i, sql_col in enumerate(filter_value):
        view_table.setItem(0, i, QTableWidgetItem(filter_value[sql_col]))

def get_new_value_from_view(page):
    view_table = page.findChildren(QTableWidget, "view_table")[0]

    return

def get_filter_values(page, num_row):
    pass

def update(page):
    new_value = get_new_value_from_view(page)
    filter_value = get_filter_values(page, 0)
    sql_table = ...
    sql_query_update(page.db_con, sql_table, new_value, filter_value)


def setup_update_settings_layout(page, sql_table):
    settings_layout = page.settings_action_layout
    settings_layout.clear_layout()

    settings_label = QLabel(f"<b>Принять обновление для {sql_table.name}</b>")
    settings_layout.addWidget(settings_label)

    accept_update_btn = QPushButton("Обновить запись")
    accept_update_btn.clicked.connect(partial(update, page))
    settings_layout.addWidget(accept_update_btn)