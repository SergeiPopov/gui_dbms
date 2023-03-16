import sqlalchemy as sl


def get_tables_list(db_con, specified_schema=None):
    inspector = sl.inspect(db_con)
    tables = inspector.get_table_names(schema=specified_schema)
    return tables

def update_settings_layout():
    pass

def update_view_layout():
    pass