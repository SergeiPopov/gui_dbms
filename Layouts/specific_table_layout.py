from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Layouts.Layout import Layout


def _init_specific_table_layout(page):
    # Раздел для функциональных кнопок для конкретной таблицы
    specific_action_layout = Layout(QBoxLayout.Direction.TopToBottom, page)

    specific_label = QLabel("<h3><b>Работа с указанной таблицей и схемой</b></h3>")

    # Строки для ввода названия таблицы или схемы
    table_name_layout = QHBoxLayout()
    table_name_label = QLabel("Введите название таблицы")
    table_name_line_edit = QLineEdit(parent=page)
    table_name_line_edit.setObjectName("table_name_line_edit")
    table_name_layout.addWidget(table_name_label)
    table_name_layout.addWidget(table_name_line_edit)

    schema_name_layout = QHBoxLayout()
    schema_name_label = QLabel("Введите название схемы")
    schema_name_line_edit = QLineEdit(parent=page)
    schema_name_line_edit.setObjectName("schema_name_line_edit")
    schema_name_layout.addWidget(schema_name_label)
    schema_name_layout.addWidget(schema_name_line_edit)

    # Функциональные кнопки для указанной таблицы
    get_table_columns_info_btn = QPushButton("Вывести информацию о таблице", page)
    get_table_columns_info_btn.setObjectName("get_table_columns_info_btn")

    get_table_rows_btn = QPushButton("Вывести записи таблицы", page)
    get_table_rows_btn.setObjectName("get_table_rows_btn")

    # Функциональные кнопки для указанной схемы
    get_tables_btn = QPushButton("Получить список таблиц", page)
    get_tables_btn.setObjectName("get_tables_btn")

    specific_action_layout.addWidget(specific_label)
    specific_action_layout.addLayout(table_name_layout)
    specific_action_layout.addLayout(schema_name_layout)
    specific_action_layout.addWidget(get_tables_btn)
    specific_action_layout.addWidget(get_table_columns_info_btn)
    specific_action_layout.addWidget(get_table_rows_btn)

    return specific_action_layout
