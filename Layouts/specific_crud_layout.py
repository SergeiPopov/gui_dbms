from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Layouts.Layout import Layout


def _init_specific_crud_layout(page):
    # Раздел общего назначения для функциональных кнопок
    specific_crud_layout = Layout(QBoxLayout.Direction.TopToBottom, page)

    specific_label = QLabel("<h3><b>CRUD с указанной таблицей и схемой</b></h3>")

    # Кнопки crud для определенной таблицы
    create_rows_by_table_btn = QPushButton("Создать несколько записей из таблицы", page)
    create_rows_by_table_btn.setObjectName("create_rows_by_table_btn")

    update_rows_by_table_btn = QPushButton("Обновить несколько записей из таблицы", page)
    update_rows_by_table_btn.setObjectName("update_rows_by_table_btn")

    delete_rows_by_table_btn = QPushButton("Удалить несколько записей из таблицы", page)
    delete_rows_by_table_btn.setObjectName("delete_rows_by_table_btn")

    specific_crud_layout.addWidget(specific_label)
    specific_crud_layout.addWidget(create_rows_by_table_btn)
    specific_crud_layout.addWidget(update_rows_by_table_btn)
    specific_crud_layout.addWidget(delete_rows_by_table_btn)

    return specific_crud_layout
