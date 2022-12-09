import os

import numpy as np
import pandas as pd
from Services.Db.DbContext import DbContext


class DbService:
    @staticmethod
    def execute(query):
        context = DbContext()

        context.cursor.execute(query)
        context.db.commit()
        context.db.close()

    @staticmethod
    def select(query):
        context = DbContext()

        context.cursor.execute(query)
        result = context.cursor.fetchall()

        return result

    @staticmethod
    def get_table_csv(table_name):
        context = DbContext()
        connection = context.db
        supplier_folder = table_name.upper()
        path = os.path.join('../TemporaryStorage', supplier_folder, 'export')
        out_file_path = os.path.join(path, f'export.csv')
        if not os.path.exists(path):
            os.makedirs(path)

        table_df = pd.read_sql_query(' SELECT manufacturer, supplier_part_number, '
                                        ' IFNULL(part_number, supplier_part_number) as part_number, '
                                        ' CAST(quantity AS INTEGER) as quantity, '
                                        ' ROUND(price, 2) as price, '
                                        ' CAST(IFNULL(delivery, 404) AS INTEGER) AS delivery '
                                        f' FROM {table_name} '
                                        ' WHERE quantity > 0 AND price > 0',
                                         connection)
        table_df.to_csv(out_file_path , sep=';', index=False)

        return out_file_path

    @staticmethod
    def get_table_csv_big(table_name, table):
        context = DbContext()
        connection = context.db
        supplier_folder = table_name.upper()
        path = os.path.join('../TemporaryStorage', supplier_folder, 'export')
        out_file_path = os.path.join(path, f'export.csv')
        if not os.path.exists(path):
            os.makedirs(path)

        table_df = pd.DataFrame()
        table_df['manufacturer'] = table['manufacturer']
        table_df['supplier_part_number'] = table['supplier_part_number']
        table_df['part_number'] = table['part_number']
        table_df['quantity'] = table['quantity'].astype(int)
        table_df['price'] = \
            table['price'].astype(str).str.replace(',', '').astype(float).round(decimals=2)
        # table_df['delivery'] = table['delivery']
        table_df['delivery'] = np.where(table['delivery'].isnull(), 404, table['delivery'])

        table_df.to_csv(out_file_path, sep=';', index=False)

        return out_file_path

    @staticmethod
    def get_db_backup():
        print('Pushing backup file to ftp')
        context = DbContext()
        connection = context.db
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        dfs = []
        i = 1
        for table in tables:
            supplier = table[0]
            print(f'getting {supplier} ...')
            print(f'complited {i}/{len(tables)}')
            i = i+1
            table_df = pd.read_sql_query(' SELECT "{}" as supplier, ' 
                                         ' manufacturer, supplier_part_number, '
                                         ' part_number, CAST(quantity AS INTEGER) as quantity, '
                                         ' ROUND(price, 2) as price '
                                         ' FROM {} '.format(supplier, table[0]),
                                         connection)
            dfs.append(table_df)
        out = pd.concat(dfs, ignore_index=False)
        out.to_sql(f'db_full', connection, if_exists='replace', index=False)
        #ftp = FtpConnection('138.201.56.185', 'ph6802', 'z7lIh8iv10pLRt')
        #ftp.upload_backup('../Database/mnk_base.db')



