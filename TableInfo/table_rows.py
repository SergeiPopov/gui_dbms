from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy as sl

from Layouts import Layout


def get_table_rows(db_con, selected_cols: list, limit: int, offset: int, group_by_for_first_col: True):
    if not len(selected_cols):
        return None

    select_query = sl.select(*selected_cols) \
        .limit(limit) \
        .offset(offset)

    # Запрос с лимитом в MSSQL нельзя без группировки
    if group_by_for_first_col:
        select_query.group_by(selected_cols[0])

    curs = db_con.execute(select_query)
    return curs.keys(), curs.all()


def get_settings_from_layout(settings_layout: Layout):
    return settings_layout.findChildren(QLabel, "limit_line_edit")



def setup_settings_layout(db_con, settings_layout: Layout, limit: int, offset: int, table_name: str, schema=None):
    inspector = sl.inspect(db_con)

    settings_layout.clear_layout()

    limit_line_edit = QLineEdit(limit, settings_layout)
    limit_line_edit.setObjectName("limit_line_edit")

    offset_line_edit = QLineEdit(offset, settings_layout)
    offset_line_edit.setObjectName("offset_line_edit")

    # Добавление списка колонок таблицы
    checkbox_columns_list = QListWidget(settings_layout)
    checkbox_columns_list.setObjectName("checkbox_columns_list")
    columns = inspector.get_columns(table_name, schema=schema)
    for col in columns:
        checkbox_column = QListWidgetItem(col['name'])
        checkbox_column.setCheckState(Qt.CheckState.Checked)
        checkbox_columns_list.addItem(checkbox_column)

    # Кнопка для запуска запроса
    get_table_rows_btn = QPushButton("Показать записи таблицы", settings_layout)
    get_table_rows_btn.setObjectName("get_table_rows_btn")

    settings_layout.addWidget(limit_line_edit)
    settings_layout.addWidget(offset_line_edit)
    settings_layout.addWidget(checkbox_columns_list)
    settings_layout.addWidget(get_table_rows_btn)


