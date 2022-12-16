import pandas as pd
from threading import Thread, active_count
from api.Services.Db.DbContext import DbContext
from api.Services.Db.DbService import DbService
from api.Utils.consts import CONSOLE_COLOR, PATHS, ERRORS
from api.Services.Ftp.FtpConnection import FtpConnection
import datetime


def format_column(column: pd.Series):
    column = column.str.upper()
    column = column.str.replace('[\W_]+', '', regex=True)
    column = column.str.strip()
    return column


class DataFrameReader:
    @staticmethod
    def dataframe_to_db(table_name, dataframe):
        context = DbContext()
        connection = context.db
        dataframe['part_number'] = format_column(dataframe['part_number'])
        dataframe['manufacturer'] = dataframe['manufacturer'].str.upper()
        dataframe['timestamp'] = datetime.datetime.today().strftime('%d-%m-%Y')
        dataframe.to_sql(table_name, connection, if_exists='replace', index=False)
        DataFrameReader.supplier_to_ftp(table_name)

    @staticmethod
    def supplier_to_ftp(supplier):
        db = DbService()
        print('Exporting {} to csv'.format(supplier))
        file = db.get_table_csv(supplier)
        ftp = FtpConnection('138.201.56.185', 'ph6802', 'z7lIh8iv10pLRt')
        ftp.upload_file(file, 'maxi_export', supplier)

    @staticmethod
    def dataframe_to_db_big(table_name, dataframe):
        context = DbContext()
        connection = context.db
        dataframe['part_number'] = format_column(dataframe['part_number'])
        dataframe['timestamp'] = datetime.datetime.today().strftime('%d-%m-%Y')
        dataframe.to_sql(table_name, connection, if_exists='replace', index=False)
        DataFrameReader.supplier_to_ftp_big(table_name, dataframe)

    @staticmethod
    def supplier_to_ftp_big(supplier, dataframe):
        db = DbService()
        print('Exporting {} to csv'.format(supplier))
        file = db.get_table_csv_big(supplier, dataframe)
        ftp = FtpConnection('138.201.56.185', 'ph6802', 'z7lIh8iv10pLRt')
        ftp.upload_file(file, 'maxi_export', supplier)

    @staticmethod
    def dataframe_to_db_orap(table_name, dataframe):
        context = DbContext()
        connection = context.db
        dataframe['part_number'] = format_column(dataframe['part_number'])
        dataframe['timestamp'] = datetime.datetime.today().strftime('%d-%m-%Y')
        dataframe.to_sql(table_name, connection, if_exists='replace', index=False)
        # DataFrameReader.supplier_to_ftp_big(table_name, dataframe)
