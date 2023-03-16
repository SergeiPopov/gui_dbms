from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class Layout(QBoxLayout):
    def __init__(self, direction: QBoxLayout.Direction, parent=None):
        super(Layout, self).__init__(direction, parent)

    def clear_layout(self):
        # Удаление элементов внутри слоя
        list_items = list()
        for i_widget in range(self.count()):
            item = self.itemAt(i_widget)
            list_items.append(item)

        for item in list_items:
            item.widget().deleteLater()
            self.removeItem(item)
            del item

    def append(self, widget):
        self.addWidget(widget)

