from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Layouts.Layout import Layout


def _init_settings_action_layout(page):
    # Раздел для настроек конкретного действия
    settings_layout = Layout(QBoxLayout.Direction.TopToBottom, page)

    label = QLabel("<b>Настройка для действия</b>")

    settings_layout.addWidget(label)

    return settings_layout
