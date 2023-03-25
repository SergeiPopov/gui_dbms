import sqlalchemy
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy as sl

from Layouts import Layout
from functools import partial
from CRUD import delete_row
from TableFuncs.table_info import get_table

def get_table_rows(db_con, selected_cols: list, limit: int, offset: int, filter_dict: dict, group_by_for_first_col=True):
    if not len(selected_cols):
        return None

    select_query = sl.select(*selected_cols) \
        .limit(limit) \
        .offset(offset)

    # Запрос с лимитом в MSSQL нельзя без группировки
    if group_by_for_first_col:
        select_query = select_query.order_by(selected_cols[0])

    for col in filter_dict:
        select_query = select_query.where(col == filter_dict[col])

    curs = db_con.execute(select_query)
    return curs.all(), curs.keys()


def update_rows_from_settings_layout(page):
    db_con = page.db_con
    limit = int(page.findChildren(QLineEdit, "limit_line_edit")[0].text())
    offset = int(page.findChildren(QLineEdit, "offset_line_edit")[0].text())
    table_name = page.findChildren(QLabel, "table_name_label")[0].text().split(" ")[-1]
    schema = page.findChildren(QLabel, "table_name_label")[0].text().split(" ")[-2]
    schema = None if schema == "" else schema

    meta = sqlalchemy.MetaData(schema=schema)
    table = sqlalchemy.Table(table_name, meta, autoload_with=db_con.engine)

    selected_cols = list()
    filter_dict = dict()
    checkbox_list = page.findChildren(QVBoxLayout, "checkbox_columns_list")[0]
    for i_check_box in range(checkbox_list.count()):
        layout_check_and_filter = checkbox_list.itemAt(i_check_box)
        check_box = layout_check_and_filter.itemAt(0).widget()
        filter_line = layout_check_and_filter.itemAt(1).widget()
        if check_box.checkState() == Qt.CheckState.Checked:
            col = getattr(table.c, check_box.text())
            selected_cols.append(col)
            if filter_line.text():
                filter_dict[col] = filter_line.text()

    rows, columns_names = get_table_rows(db_con, selected_cols, limit, offset, filter_dict)
    set_view_table_rows(page, rows, columns_names)


def set_view_table_rows(page, rows, columns_names):
    view_table = page.findChildren(QTableWidget, "view_table")[0]
    columns_names = list(columns_names)
    # Колонки для кнопок
    columns_names.append('Удалить запись')
    columns_names.append('Обновить запись')

    view_table.setRowCount(len(rows))
    view_table.setColumnCount(len(columns_names))
    view_table.setHorizontalHeaderLabels(columns_names)

    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            view_table.setItem(i, j, QTableWidgetItem(str(cell)))
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(partial(delete_clicked_view_table_btn, page, i))

        update_btn = QPushButton("Обновить")
        # update_btn.clicked.connect()
        view_table.setCellWidget(i, len(row), delete_btn)
        view_table.setCellWidget(i, len(row) + 1, update_btn)


def delete_clicked_view_table_btn(page, num_row):
    db_con = page.db_con
    table_name = page.findChildren(QLineEdit, "table_name_line_edit")[0].text()
    schema_name = page.findChildren(QLineEdit, "schema_name_line_edit")[0].text()
    view_table = page.findChildren(QTableWidget, "view_table")[0]

    sql_table = get_table(db_con, table_name, schema_name)

    for num_col in range(view_table.columnCount() - 2):
        print(view_table.item(num_row, num_col).text())


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
    layout_check_and_line_rows = QVBoxLayout()
    layout_check_and_line_rows.setObjectName("checkbox_columns_list")
    columns = inspector.get_columns(table_name, schema=schema)
    for col in columns:
        check_and_line_row = QHBoxLayout()

        col_check = QCheckBox(col['name'])
        col_check.setCheckState(Qt.CheckState.Checked)

        col_filter = QLineEdit()

        check_and_line_row.addWidget(col_check)
        check_and_line_row.addWidget(col_filter)

        layout_check_and_line_rows.addLayout(check_and_line_row)


    # Кнопка для запуска запроса
    get_table_rows_btn = QPushButton("Вывести записи таблицы", page)
    get_table_rows_btn.setObjectName("update_table_rows_btn")
    get_table_rows_btn.clicked.connect(partial(update_rows_from_settings_layout, page))

    settings_layout.addWidget(settings_label)
    settings_layout.addWidget(table_name_label)
    settings_layout.addWidget(limit_line_edit)
    settings_layout.addWidget(offset_line_edit)
    settings_layout.addWidget(QLabel("Фильтр по колонкам"))
    settings_layout.addLayout(layout_check_and_line_rows)
    settings_layout.addWidget(get_table_rows_btn)


