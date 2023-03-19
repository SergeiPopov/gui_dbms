from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy

from Layouts.Layout import Layout
from TableFuncs import table_rows, tables_list, schema_list, table_info


class TableInfoPage(QWidget):
    def __init__(self, db_con, parent=None):
        super(TableInfoPage, self).__init__(parent)

        self.db_con = db_con
        self.main_grid = QGridLayout(self)

        self.general_action_layout = self._init_general_action_layout()
        self.specific_action_layout = self._init_specific_action_layout()
        self.view_layout = self._init_view_layout()
        self.settings_action_layout = self._init_settings_action_layout()

        self.main_grid.addLayout(self.general_action_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
        self.main_grid.addLayout(self.specific_action_layout, 1, 0, Qt.AlignmentFlag.AlignTop)
        self.main_grid.addLayout(self.view_layout, 0, 1, 2, 1)
        self.main_grid.addLayout(self.settings_action_layout, 0, 2, 2, 1, Qt.AlignmentFlag.AlignTop)
        self.main_grid.setColumnStretch(1, 2)

    def _init_specific_action_layout(self):
        # Раздел для функциональных кнопок для конкретной таблицы
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

        # Функциональные кнопки для указанной таблицы
        get_table_columns_info_btn = QPushButton("Вывести информацию о таблице", self)
        get_table_columns_info_btn.setObjectName("get_table_columns_info")
        get_table_columns_info_btn.clicked.connect(self.get_table_columns_info)

        get_table_rows_btn = QPushButton("Вывести записи заблицы", self)
        get_table_rows_btn.setObjectName("get_table_rows_btn")
        get_table_rows_btn.clicked.connect(self.get_tables_rows)

        # Функциональные кнопки для указанной схемы
        get_tables_btn = QPushButton("Получить список таблиц", self)
        get_tables_btn.setObjectName("get_tables_btn")
        get_tables_btn.clicked.connect(self.get_table_list)

        specific_action_layout.addWidget(specific_label)
        specific_action_layout.addLayout(table_name_layout)
        specific_action_layout.addLayout(schema_name_layout)
        specific_action_layout.addWidget(get_tables_btn)
        specific_action_layout.addWidget(get_table_columns_info_btn)
        specific_action_layout.addWidget(get_table_rows_btn)

        return specific_action_layout

    def _init_general_action_layout(self):
        # Раздел общего назначения для функциональных кнопок
        general_action_layout = Layout(QBoxLayout.Direction.TopToBottom, self)

        # Кнопки общего назначения
        get_schemas_btn = QPushButton("Получить список схем", self)
        get_schemas_btn.setObjectName("get_schemas_btn")
        get_schemas_btn.clicked.connect(self.get_schemas_list)

        general_action_layout.addWidget(get_schemas_btn)

        return general_action_layout

    def _init_view_layout(self):
        # Раздел таблица для отображения строк, информации о таблице и тд (Всё что можно представить в виде таблицы)
        view_layout = Layout(QBoxLayout.Direction.TopToBottom, self)

        view_table = QTableWidget(self)
        view_table.setObjectName("view_table")

        view_layout.addWidget(view_table)

        return view_layout

    def _init_settings_action_layout(self):
        # Раздел для настроек конкретного действия
        settings_layout = Layout(QBoxLayout.Direction.TopToBottom, self)

        label = QLabel("<b>Настройка для действия</b>")

        settings_layout.addWidget(label)

        return settings_layout

    def get_table_list(self):
        schema_name = self.findChildren(QLineEdit, "schema_name_line_edit")[0].text()
        schema_name = None if schema_name == "" else schema_name
        tables = tables_list.get_tables_list(self.db_con, specified_schema=schema_name)
        tables_list.set_view_tables_list(self.findChildren(QTableWidget, "view_table")[0], tables)

    def get_schemas_list(self):
        schemas = schema_list.get_schemas_list(self.db_con)
        view_table = self.findChildren(QTableWidget, "view_table")[0]
        schema_list.set_view_schemas_list(view_table, schemas)

    def get_tables_rows(self):
        schema_name = self.findChildren(QLineEdit, "schema_name_line_edit")[0].text()
        schema_name = None if schema_name == "" else schema_name
        table_rows.setup_settings_layout(self.db_con,
                                                self,
                                                100,
                                                0,
                                                self.findChildren(QLineEdit, "table_name_line_edit")[0].text(),
                                                schema_name)

        table_rows.update_rows_from_settings_layout(self.db_con, self)


    def get_table_columns_info(self):
        columns = table_info.get_table_info(self.db_con,
                                  self.findChildren(QLineEdit, "table_name_line_edit")[0].text(),
                                  self.findChildren(QLineEdit, "schema_name_line_edit")[0].text())
        view_table = self.findChildren(QTableWidget, "view_table")[0]
        table_info.set_view_table_columns_info(view_table, columns)

    # def _update_table_rows_from_settings(self):
    #     table_rows.update_rows_from_settings_layout(self.db_con, self)
    #     pass


if __name__ == '__main__':
    db_eng = sqlalchemy.create_engine("mssql+pyodbc://SA:libdev2023@127.0.0.1:1433/books_19?driver=ODBC+Driver+17+for+SQL+Server&encrypt=no")
    db_con = db_eng.connect()

    import sys
    app = QApplication([])
    w = QMainWindow()
    main_win = TableInfoPage(db_con)
    w.setCentralWidget(main_win)

    w.show()
    sys.exit(app.exec())