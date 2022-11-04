import os
import pandas as pd
import datetime
from Services.Db.DbContext import DbContext
from Services.Ftp.FtpConnection import  FtpConnection

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
        out_file_path = os.path.join(path, 'export.csv')
        if not os.path.exists(path):
            os.makedirs(path)

        table_df = pd.read_sql_query(' SELECT manufacturer, supplier_part_number, '
                                     ' part_number, CAST(quantity AS INTEGER) as quantity, '
                                     ' ROUND(price, 2) as price '
                                     ' FROM {} '
                                     ' WHERE quantity > 0 AND price > 0'.format(table_name),
                                     connection)
        table_df.groupby(['manufacturer', 'supplier_part_number', 'part_number', 'price']).sum()
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
            table_df.groupby(['manufacturer', 'supplier_part_number', 'part_number', 'price']).sum()
            dfs.append(table_df)
        out = pd.concat(dfs, ignore_index=False)
        today = datetime.datetime.today().strftime('%Y_%m_%d')
        out_path = '../Backup'
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        file = f'{out_path}/backup_{today}.csv'
        out.to_csv(file, sep=';', index=False)
        ftp = FtpConnection('138.201.56.185', 'ph6802', 'z7lIh8iv10pLRt')
        ftp.upload_backup(file)



