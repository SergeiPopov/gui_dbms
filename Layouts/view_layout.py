from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Layouts.Layout import Layout

def _init_view_layout(page):
    # Раздел таблица для отображения строк, информации о таблице и тд (Всё что можно представить в виде таблицы)
    view_layout = Layout(QBoxLayout.Direction.TopToBottom, page)

    view_table = QTableWidget(page)
    view_table.setObjectName("view_table")

    view_layout.addWidget(view_table)

    return view_layout
