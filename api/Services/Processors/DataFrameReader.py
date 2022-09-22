from api.Services.Db.DbContext import DbContext

import pandas as pd


class DataFrameReader:

    @staticmethod
    def format_column(column: pd.Series):
        column = column.str.upper()
        column = column.str.replace('[\W_]+', '', regex=True)
        return column

    @staticmethod
    def dataframe_to_db(table_name, dataframe):
        context = DbContext()
        connection = context.db
        dataframe.to_sql(table_name, connection, if_exists='replace', index=False)