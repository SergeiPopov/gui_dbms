from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy

from Layouts.Layout import Layout
from TableFuncs import table_info
from CRUD import delete_row


class CRUDPage(QWidget):
    def __init__(self, db_con, parent=None):
        super(CRUDPage, self).__init__(parent)

        self.db_con = db_con

        self.main_grid = QGridLayout(self)
        self.specific_action_layout = self._init_specific_action_layout()
        self.view_layout = self._init_view_layout()
        self.settings_action_layout = self._init_settings_action_layout()

        self.main_grid.addLayout(self.specific_action_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
        self.main_grid.setColumnStretch(0, 0)

        self.main_grid.addLayout(self.view_layout, 0, 1, 2, 1)
        self.main_grid.setColumnStretch(1, 1)

        self.main_grid.addLayout(self.settings_action_layout, 0, 2, 2, 1, Qt.AlignmentFlag.AlignTop)
        self.main_grid.setColumnStretch(2, 0)

    def _init_specific_action_layout(self):
        # Раздел общего назначения для функциональных кнопок
        specific_action_layout = Layout(QBoxLayout.Direction.TopToBottom, self)

        specific_label = QLabel("<h3><b>Работа с указанной таблицей и/или схемой</b></h3>")

        # Строки для ввода названия таблицы или схемы
        table_name_layout = QHBoxLayout()
        table_name_label = QLabel("Введите название таблицы")
        table_name_line_edit = QLineEdit()
        table_name_line_edit.setObjectName("table_name_line_edit")
        table_name_line_edit.setParent(self)
        table_name_layout.addWidget(table_name_label)
        table_name_layout.addWidget(table_name_line_edit)

        schema_name_layout = QHBoxLayout()
        schema_name_label = QLabel("Введите название схемы")
        schema_name_line_edit = QLineEdit()
        schema_name_line_edit.setObjectName("schema_name_line_edit")
        schema_name_line_edit.setParent(self)
        schema_name_layout.addWidget(schema_name_label)
        schema_name_layout.addWidget(schema_name_line_edit)

        # Кнопки общего назначения
        delete_rows_by_table_btn = QPushButton("Удалить несколько записей из таблицы", self)
        delete_rows_by_table_btn.setObjectName("delete_rows_by_table_btn")
        delete_rows_by_table_btn.clicked.connect(self.delete_rows_by_table)

        update_rows_by_table_btn = QPushButton("Обновить несколько записей из таблицы", self)
        update_rows_by_table_btn.setObjectName("update_rows_by_table_btn")
        # update_rows_by_table_btn.clicked.connect(self.update_rows_by_table)

        specific_action_layout.addWidget(specific_label)
        specific_action_layout.addLayout(table_name_layout)
        specific_action_layout.addLayout(schema_name_layout)
        specific_action_layout.addWidget(delete_rows_by_table_btn)
        specific_action_layout.addWidget(update_rows_by_table_btn)

        return specific_action_layout

    def _init_view_layout(self):
        view_layout = Layout(QBoxLayout.Direction.TopToBottom, self)

        view_table = QTableWidget(self)
        view_table.setObjectName("view_table")

        view_layout.addWidget(view_table)
        # Добавление строки
        # view_table.insertRow(view_table.rowCount())
        return view_layout

    def _init_settings_action_layout(self):
        # Раздел для настроек конкретного действия
        settings_layout = Layout(QBoxLayout.Direction.TopToBottom, self)

        label = QLabel("<b>Настройка для действия</b>")

        settings_layout.addWidget(label)

        return settings_layout

    def delete_rows_by_table(self):
        view_table = self.findChildren(QTableWidget, "view_table")[0]
        table_name = self.findChildren(QLineEdit, "table_name_line_edit")[0].text()
        schema = self.findChildren(QLineEdit, "schema_name_line_edit")[0].text()
        schema = schema if schema else None
        sql_table = table_info.get_table(self.db_con, table_name, schema)
        columns = table_info.get_table_info(self.db_con, table_name, schema)
        delete_row.set_view_delete_row(view_table, columns)
        delete_row.setup_settings_layout(self.settings_action_layout, self.db_con, view_table, sql_table)


if __name__ == '__main__':
    db_eng = sqlalchemy.create_engine("mssql+pyodbc://SA:libdev2023@127.0.0.1:1433/normal_marc?driver=ODBC+Driver+17+for+SQL+Server&encrypt=no", echo=True)
    db_con = db_eng.connect()

    import sys
    app = QApplication([])
    w = QMainWindow()
    main_win = CRUDPage(db_con)
    w.setCentralWidget(main_win)

    w.show()
    sys.exit(app.exec())