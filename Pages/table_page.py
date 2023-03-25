from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy

import Layouts
from TableFuncs import table_rows, tables_list, schema_list, table_info


class TableInfoPage(QWidget):
    def __init__(self, db_con, parent=None):
        super(TableInfoPage, self).__init__(parent)

        self.db_con = db_con
        self.main_grid = QGridLayout(self)

        self.general_action_layout = Layouts._init_general_action_layout(self)
        self.specific_crud_layout = Layouts._init_specific_crud_layout(self)
        self.specific_table_layout = Layouts._init_specific_table_layout(self)
        self.view_layout = Layouts._init_view_layout(self)
        self.settings_action_layout = Layouts._init_settings_action_layout(self)

        self.main_grid.addLayout(self.general_action_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
        self.main_grid.addLayout(self.specific_table_layout, 1, 0, Qt.AlignmentFlag.AlignTop)
        self.main_grid.addLayout(self.specific_crud_layout, 2, 0, Qt.AlignmentFlag.AlignTop)
        self.main_grid.addLayout(self.view_layout, 0, 1, 3, 1)
        self.main_grid.addLayout(self.settings_action_layout, 0, 2, 3, 1, Qt.AlignmentFlag.AlignTop)
        self.main_grid.setColumnStretch(1, 2)

        self.connect_buttons()

    def connect_buttons(self):
        get_schemas_btn = self.findChildren(QPushButton, "get_schemas_btn")[0]
        get_schemas_btn.clicked.connect(self.get_schemas_list)

        get_table_columns_info_btn = self.findChildren(QPushButton, "get_table_columns_info_btn")[0]
        get_table_columns_info_btn.clicked.connect(self.get_table_columns_info)

        get_table_rows_btn = self.findChildren(QPushButton, "get_table_rows_btn")[0]
        get_table_rows_btn.clicked.connect(self.get_tables_rows)

        get_tables_btn = self.findChildren(QPushButton, "get_tables_btn")[0]
        get_tables_btn.clicked.connect(self.get_table_list)

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

        table_rows.update_rows_from_settings_layout(self)

    def get_table_columns_info(self):
        columns = table_info.get_table_info(self.db_con,
                                  self.findChildren(QLineEdit, "table_name_line_edit")[0].text(),
                                  self.findChildren(QLineEdit, "schema_name_line_edit")[0].text())
        view_table = self.findChildren(QTableWidget, "view_table")[0]
        table_info.set_view_table_columns_info(view_table, columns)


if __name__ == '__main__':
    db_eng = sqlalchemy.create_engine("mssql+pyodbc://SA:libdev2023@127.0.0.1:1433/normal_marc?driver=ODBC+Driver+17+for+SQL+Server&encrypt=no")
    db_con = db_eng.connect()

    import sys
    app = QApplication([])
    w = QMainWindow()
    w.setGeometry(100, 100, 1200, 600)
    main_win = TableInfoPage(db_con)
    w.setCentralWidget(main_win)

    w.show()
    sys.exit(app.exec())