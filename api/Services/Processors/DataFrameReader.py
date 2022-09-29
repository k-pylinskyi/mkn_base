from api.Services.Db.DbContext import DbContext

import pandas as pd


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
        dataframe.to_sql(table_name, connection, if_exists='replace', index=False)
