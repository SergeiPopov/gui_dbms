import sqlalchemy

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


def get_schemas_list(db_con):
    inspector = sqlalchemy.inspect(db_con)
    schemas = inspector.get_schema_names()
    return schemas


def set_view_schemas_list(view_table, schemas_list: list):
    view_table.setRowCount(len(schemas_list))
    view_table.setColumnCount(1)
    view_table.setHorizontalHeaderLabels(["Название схемы"])

    for i, schema in enumerate(schemas_list):
        view_table.setItem(i, 0, QTableWidgetItem(schema))