from functools import partial

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from common_func.def_msg_box import DefMsgBox


def sql_query_update(db_con, sql_table, new_value, filter_value):
    update_query = sql_table.update()

    for col in filter_value:
        update_query = update_query.where(col == filter_value[col])

    update_query = update_query.values(new_value)

    db_con.execute(update_query)
    db_con.commit()


def set_view_update_row(page, columns_names, filter_value):
    view_table = page.findChildren(QTableWidget, "view_table")[0]
    view_table.clear()
    view_table.setRowCount(2)
    view_table.setColumnCount(len(columns_names))
    view_table.setHorizontalHeaderLabels(columns_names)
    view_table.setVerticalHeaderLabels(["Фильтр пред. записи", "Обновленные записи"])

    for i, sql_col in enumerate(filter_value):
        view_table.setItem(0, i, QTableWidgetItem(filter_value[sql_col]))


def get_new_value_from_view(page, sql_table) -> dict:
    view_table = page.findChildren(QTableWidget, "view_table")[0]

    new_col_value_dict = dict()
    for num_col in range(view_table.columnCount()):
        item_value = view_table.item(1, num_col)
        if item_value:
            sql_col = view_table.horizontalHeaderItem(num_col).text()
            new_col_value_dict[sql_col] = item_value.text()

    return new_col_value_dict


def get_filter_values(page, sql_table):
    view_table = page.findChildren(QTableWidget, "view_table")[0]

    filter_col_value_dict = dict()
    for num_col in range(view_table.columnCount()):
        item_value = view_table.item(0, num_col)
        if item_value:
            sql_col = getattr(sql_table.c, view_table.horizontalHeaderItem(num_col).text())
            filter_col_value_dict[sql_col] = item_value.text()

    return filter_col_value_dict


def update(page, sql_table):
    try:
        new_value = get_new_value_from_view(page, sql_table)
        filter_value = get_filter_values(page, sql_table)
        sql_query_update(page.db_con, sql_table, new_value, filter_value)
        DefMsgBox("Обновлено", "Запись была успешно обновлена")
    except:
        DefMsgBox("Ошибка обновления", "Что то пошло не так. Запись не была обновлена")



def setup_update_settings_layout(page, sql_table):
    settings_layout = page.settings_action_layout
    settings_layout.clear_layout()

    settings_label = QLabel(f"<b>Принять обновление для {sql_table.name}</b>")
    settings_layout.addWidget(settings_label)

    accept_update_btn = QPushButton("Обновить запись")
    accept_update_btn.clicked.connect(partial(update, page, sql_table))
    settings_layout.addWidget(accept_update_btn)


