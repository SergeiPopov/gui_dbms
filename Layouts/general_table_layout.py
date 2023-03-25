from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Layouts.Layout import Layout


def _init_general_action_layout(page):
    # Раздел общего назначения для функциональных кнопок
    general_action_layout = Layout(QBoxLayout.Direction.TopToBottom, page)

    # Кнопки общего назначения
    get_schemas_btn = QPushButton("Получить список схем", page)
    get_schemas_btn.setObjectName("get_schemas_btn")
    # get_schemas_btn.clicked.connect(page.get_schemas_list)

    general_action_layout.addWidget(get_schemas_btn)

    return general_action_layout