import os
import pandas as pd
from api.Services.Db.DbContext import DbContext


def connect():
    db = DbService()
    db.initial_create()


class DbService:

    def __init__(self):
        self.sql_create_dir = './SqlScripts/InitialCreate/Create'
        self.sql_create_view_dir = './SqlScripts/InitialCreate/CreateView'
        self.sql_insert_dir = './SqlScripts/InitialCreate/Insert'
        self.sql_select_dir = './SqlScripts/Select'
        self.create_query_list = os.listdir(self.sql_create_dir)
        self.insert_query_list = os.listdir(self.sql_insert_dir)

    def initial_create(self):
        context = DbContext()
        # Creating db tables loop
        for query in self.create_query_list:
            full_path = os.path.join(self.sql_create_dir, query)
            sql_file = open(full_path)
            query_string = sql_file.read()

            print('------')
            print(query)
            print('------')
            print(query_string)

            context.cursor.execute(query_string)
            context.db.commit()
        context.db.close()
        # Inserting db tables data loop
        for query in self.insert_query_list:
            print(query)
            self.insert(query)

    def insert(self, query):
        context = DbContext()

        full_path = os.path.join(self.sql_insert_dir, query)
        sql_file = open(full_path)
        query_string = sql_file.read()

        context.cursor.execute(query_string)
        context.db.commit()
        context.db.close()

    def select(self, query):
        context = DbContext()

        full_path = os.path.join(self.sql_select_dir, query)
        sql_file = open(full_path)
        query_string = sql_file.read()

        context.cursor.execute(query_string)
        result = context.cursor.fetchall()

        return result

    def create_views(self):
        context = DbContext()

        full_path = os.path.join(self.sql_create_view_dir, 'suppliers_prices.sql')
        sql_file = open(full_path)
        query_string = sql_file.read()

        context.cursor.execute(query_string)

    def get_table_csv(self, table_name):
        context = DbContext()
        connection = context.db
        supplier_folder = table_name.upper()
        path = os.path.join('../TemporaryStorage', supplier_folder, 'export')
        out_file_path = os.path.join(path, 'export.csv')
        if not os.path.exists(path):
            os.makedirs(path)

        table_df = pd.read_sql_query('SELECT manufacturer, supplier_part_number, '
                                     'part_number, quantity, price FROM {} '
                                     'WHERE quantity > 0 AND price > 0'.format(table_name),
                                     connection)
        table_df.to_csv(out_file_path, sep=';', index=False)

        return out_file_path

