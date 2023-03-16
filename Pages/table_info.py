from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Layouts.Layout import Layout

from TableInfo import table_rows

class TableInfoPage(QGridLayout):
    def __init__(self, parent=None):
        super(TableInfoPage, self).__init__(parent)



        self._set_general_action_layout()
        self._set_specific_action_layout()
        self._set_view_layout()
        self._set_settings_action_layout()

        self.addLayout(self.general_action_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
        self.addLayout(self.specific_action_layout, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.addLayout(self.view_layout, 0, 1, 2, 1)
        self.addLayout(self.settings_layout, 0, 2, 2, 1, Qt.AlignmentFlag.AlignTop)
        self.setColumnStretch(1, 2)

        print(self.specific_action_layout.children())

    def _set_specific_action_layout(self):
        # Раздел для функциональных кнопок для конкретной таблицы
        self.specific_action_layout = Layout(QBoxLayout.Direction.TopToBottom, self.parent())

        self.specific_label = QLabel()
        self.specific_label.setText("Работа с указанной таблицей")

        # Строка для ввода названия таблицы
        self.table_name_line_edit = QLineEdit("Введите название таблицы")

        # Функциональные кнопки для указанной таблицы
        self.get_table_info_btn = QPushButton("Вывести информацию о таблице")
        self.get_table_rows_btn = QPushButton("Вывести записи заблицы")

        self.specific_action_layout.addWidget(self.specific_label)
        self.specific_action_layout.addWidget(self.table_name_line_edit)
        self.specific_action_layout.addWidget(self.get_table_info_btn)
        self.specific_action_layout.addWidget(self.get_table_rows_btn)

    def _set_general_action_layout(self):
        # Раздел общего назначения для функциональных кнопок
        self.general_action_layout = Layout(QBoxLayout.Direction.TopToBottom, self.parent())

        # Кнопки общего назначения
        self.get_tables_btn = QPushButton("Получить список таблиц")

        self.general_action_layout.addWidget(self.get_tables_btn)

    def _set_view_layout(self):
        # Раздел таблица для отображения строк, информации о таблице и тд (Всё что можно представить в виде таблицы)
        self.view_layout = Layout(QBoxLayout.Direction.TopToBottom, self.parent())
        self.view_table = QTableWidget(self.parent())

        self.view_layout.addWidget(self.view_table)

    def _set_settings_action_layout(self):
        # Раздел для настроек конкретного действия
        # self.settings_layout = Layout(QBoxLayout.Direction.TopToBottom, self.parent())

        self.settings_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom, self.widget())

        # label = QLabel("Настройка действия", self)
        # label.setObjectName("limit_line_edit")
        # self.settings_layout.addWidget(label)

        # self.settings_layout.addWidget(label)
        # self.settings_layout.addChildWidget(label)




import sys
app = QApplication([])
w = QWidget()
main_win = TableInfoPage()

w.setLayout(main_win)
# print(table_rows.get_settings_from_layout(main_win))
w.show()
sys.exit(app.exec())