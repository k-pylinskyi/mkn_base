import pandas as pd
from Services.Db.DbContext import DbContext

class DbSender:
    @staticmethod
    def send(table_name, dataframe):
        context = DbContext()
        connection = context.db
        dataframe.to_sql(table_name, connection, if_exists='replace', index=False)