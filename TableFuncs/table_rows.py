import sqlalchemy
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy as sl

from Layouts import Layout
from functools import partial


def get_table_rows(db_con, selected_cols: list, limit: int, offset: int, group_by_for_first_col=True):
    if not len(selected_cols):
        return None

    select_query = sl.select(*selected_cols) \
        .limit(limit) \
        .offset(offset)

    # Запрос с лимитом в MSSQL нельзя без группировки
    if group_by_for_first_col:
        select_query = select_query.order_by(selected_cols[0])

    curs = db_con.execute(select_query)
    return curs.all(), curs.keys()


def update_rows_from_settings_layout(db_con, page):
    limit = int(page.findChildren(QLineEdit, "limit_line_edit")[0].text())
    offset = int(page.findChildren(QLineEdit, "offset_line_edit")[0].text())
    table_name = page.findChildren(QLabel, "table_name_label")[0].text().split(" ")[-1]
    schema = page.findChildren(QLabel, "table_name_label")[0].text().split(" ")[-2]
    schema = None if schema == "" else schema

    meta = sqlalchemy.MetaData(schema=schema)
    table = sqlalchemy.Table(table_name, meta, autoload_with=db_con.engine)

    selected_cols = list()
    checkbox_list = page.findChildren(QListWidget, "checkbox_columns_list")[0]
    for i_check_box in range(checkbox_list.count()):
        state = checkbox_list.item(i_check_box).checkState()
        if state == Qt.CheckState.Checked:
            selected_cols.append(getattr(table.c, checkbox_list.item(i_check_box).text()))

    rows, columns_names = get_table_rows(db_con, selected_cols, limit, offset)
    set_view_table_rows(page.findChildren(QTableWidget, "view_table")[0], rows, columns_names)


def set_view_table_rows(view_table, rows, columns_names):
    view_table.setRowCount(len(rows))
    view_table.setColumnCount(len(columns_names))
    view_table.setHorizontalHeaderLabels(columns_names)
    # view_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            view_table.setItem(i, j, QTableWidgetItem(str(cell)))


def setup_settings_layout(db_con, page, limit: int, offset: int, table_name: str, schema=None):

    inspector = sl.inspect(db_con)
    settings_layout = page.settings_action_layout
    settings_layout.clear_layout()

    settings_label = QLabel("<b>Настройка для действия</b>")

    table_name_label = QLabel(f"Настройки записей для {schema if schema else ' '} {table_name}")
    table_name_label.setObjectName("table_name_label")

    limit_line_edit = QLineEdit(str(limit), page)
    limit_line_edit.setObjectName("limit_line_edit")

    offset_line_edit = QLineEdit(str(offset), page)
    offset_line_edit.setObjectName("offset_line_edit")

    # Добавление списка колонок таблицы
    checkbox_columns_list = QListWidget(page)
    checkbox_columns_list.setObjectName("checkbox_columns_list")
    columns = inspector.get_columns(table_name, schema=schema)
    for col in columns:
        checkbox_column = QListWidgetItem(col['name'])
        checkbox_column.setCheckState(Qt.CheckState.Checked)
        checkbox_columns_list.addItem(checkbox_column)

    # Кнопка для запуска запроса
    get_table_rows_btn = QPushButton("Обновить записи таблицы", page)
    get_table_rows_btn.setObjectName("update_table_rows_btn")
    get_table_rows_btn.clicked.connect(partial(update_rows_from_settings_layout, db_con, page))

    settings_layout.addWidget(settings_label)
    settings_layout.addWidget(table_name_label)
    settings_layout.addWidget(limit_line_edit)
    settings_layout.addWidget(offset_line_edit)
    settings_layout.addWidget(checkbox_columns_list)
    settings_layout.addWidget(get_table_rows_btn)


