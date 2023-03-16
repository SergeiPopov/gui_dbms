import sys

import sqlalchemy.exc
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sqlalchemy as sl

from Scenarios.def_msg_box import DefMsgBox


class TablePage(QWidget):
    def __init__(self, db_con, parent=None):
        super(TablePage, self).__init__(parent)
        self.db_con = db_con
        self.inspector = sl.inspect(self.db_con)
        self.metadata = sl.MetaData()
        self.engine = self.db_con.engine

        self.main_layout = QHBoxLayout(self)

        # Столбец действий
        self.action_layout = QVBoxLayout(self)
        self.get_table_list_btn = QPushButton("Получить список таблиц")
        self.get_table_list_btn.clicked.connect(self.get_tables_list)

        self.specific_actions_group = QGroupBox(self)
        self.specific_actions_group.setTitle("Работа с конкретной таблицей")
        self.specific_layout = QVBoxLayout()
        self.table_name_line = QLineEdit("", self)
        self.show_rows_btn = QPushButton("Просмотреть записи таблицы")
        self.show_rows_btn.clicked.connect(self.get_rows_from_table_name)

        self.get_table_info_btn = QPushButton("Получить информацию о таблице")
        self.get_table_info_btn.clicked.connect(self.get_table_info)

        self.specific_layout.addWidget(self.table_name_line)
        self.specific_layout.addWidget(self.show_rows_btn)
        self.specific_layout.addWidget(self.get_table_info_btn)
        self.specific_actions_group.setLayout(self.specific_layout)

        self.action_layout.addWidget(self.get_table_list_btn)
        self.action_layout.addWidget(self.specific_actions_group)

        # Столбец просмотра
        self.view_layout = QVBoxLayout()
        self.view_table = QTableWidget(self)
        self.view_layout.addWidget(self.view_table)

        # Столбец настроек для каждого действия
        self.settings_group = QGroupBox(self)
        self.settings_group.setTitle("Настройка для действия")
        self.settings_layout = QVBoxLayout()
        self.settings_group.setLayout(self.settings_layout)

        self.main_layout.addLayout(self.action_layout)
        self.main_layout.addLayout(self.view_layout)
        self.main_layout.addWidget(self.settings_group)

    def get_table_info(self):
        table_name = self.table_name_line.text()
        if table_name == '':
            DefMsgBox("Введите название таблицы", 'Ошибка подключения')
            return
        colums = self.inspector.get_columns(table_name)
        if not len(colums):
            return

        self.view_table.setRowCount(len(colums))

        self.view_table.setColumnCount(max([len(row) for row in colums]))
        self.view_table.setHorizontalHeaderLabels(colums[0].keys())
        for i, col in enumerate(colums):
            for j, info in enumerate(col):
                self.view_table.setItem(i, j, QTableWidgetItem(col.get(info).__repr__()))

    def _get_table_from_line_edit(self):
        table_name = self.table_name_line.text()
        if table_name == '':
            DefMsgBox("Введите название таблицы", 'Ошибка подключения')
            return None

        try:
            table = sl.Table(table_name, self.metadata,
                                   autoload_with=self.db_con.engine)
        except sqlalchemy.exc.NoSuchTableError:
            DefMsgBox("Вы ввели несуществующую таблицу", "Ошибка подключения")
            return None
        except:
            DefMsgBox("Что то пошло не так", "Общая ошибка")
            return None

        return table

    def get_rows_from_table_name(self):
        self.chose_table = self._get_table_from_line_edit()
        if self.chose_table != None:
            self._pre_set_settings_rows_table()
            self._update_rows_from_settings()

    def _update_rows_from_settings(self):
        selected_cols = list()
        for i_check_box in range(self.checkbox_list.count()):
            state = self.checkbox_list.item(i_check_box).checkState()
            if state == Qt.CheckState.Checked:
                selected_cols.append(getattr(self.chose_table.c, self.checkbox_list.item(i_check_box).text()))

        if not len(selected_cols):
            DefMsgBox("Веберите колонки таблицы", "Ошибка отображения таблицы")

        select_query = sl.select(*selected_cols)\
            .limit(int(self.setting_row_count_limit.text()))\
            .offset(int(self.setting_row_offset.text())).order_by(selected_cols[0])

        curs = self.db_con.execute(select_query)

        res_rows = curs.all()
        self.view_table.setRowCount(len(res_rows))
        self.view_table.setColumnCount(len(curs.keys()))
        self.view_table.setHorizontalHeaderLabels(curs.keys())
        self.view_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        for i, row in enumerate(res_rows):
            for j, cell in enumerate(row):

                self.view_table.setItem(i, j, QTableWidgetItem(str(cell)))

        # self.view_table.resizeColumnsToContents()

    def _clear_layout(self, layout):
        # Удаление элементов внутри слоя
        list_items = list()
        for i_widget in range(self.settings_layout.count()):
            item = self.settings_layout.itemAt(i_widget)
            list_items.append(item)

        for item in list_items:
            item.widget().deleteLater()
            self.settings_layout.removeItem(item)

    def _pre_set_settings_rows_table(self):
        # Удаление элементов внутри слоя
        self._clear_layout(self.settings_layout)

        self.setting_row_count_limit = QLineEdit("100", self)
        self.setting_row_offset = QLineEdit("0", self)
        self.settings_layout.addWidget(self.setting_row_count_limit)
        self.settings_layout.addWidget(self.setting_row_offset)
        self.checkbox_list = QListWidget(self)
        for col in self.chose_table.c:
            checkbox = QListWidgetItem(col.name)
            checkbox.setCheckState(Qt.CheckState.Checked)
            self.checkbox_list.addItem(checkbox)
        self.settings_layout.addWidget(self.checkbox_list)

        update_rows_btn = QPushButton("Показать записи")
        update_rows_btn.clicked.connect(self._update_rows_from_settings)
        self.settings_layout.addWidget(update_rows_btn)

    def get_tables_list(self):
        tables = self.inspector.get_table_names(schema="")
        self.view_table.setRowCount(len(tables))
        self.view_table.setColumnCount(1)
        self.view_table.setHorizontalHeaderItem(0, QTableWidgetItem(f"Таблицы схемы"))
        self.view_table.horizontalHeader().setStretchLastSection(True)
        for i, table in enumerate(tables):
            self.view_table.setItem(i, 0, QTableWidgetItem(table))


if __name__ == '__main__':
    engine = sl.create_engine(
        "mssql+pyodbc://SA:libdev2023@127.0.0.1:1433/books_19?driver=ODBC+Driver+17+for+SQL+Server&encrypt=no",
        echo=False)

    db_con = engine.connect()
    app = QApplication([])
    tp = TablePage(db_con)
    tp.show()
    sys.exit(app.exec())