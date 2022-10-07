from Services.Db.DbService import DbService
import datetime


def create_logs_table():
    query = '''
        CREATE TABLE IF NOT EXISTS 
            logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_stamp DATETIME,
                time_stamp DATETIME,
                log_type VARCHAR(20),
                log_message TEXT
            );
        '''
    DbService.execute(query)


def insert_log_to_db(date_stamp, time_stamp, log_type, log_message):
    query = f'''
        INSERT INTO logs (date_stamp, time_stamp, log_type, log_message)
        VALUES ({date_stamp}, {time_stamp}, {log_type}, {log_message});
        '''
    DbService.execute(query)

class Logger:
    @staticmethod
    def log(log_type, log_message):
        create_logs_table()
        date_stamp = datetime.date.today()
        time_stamp = datetime.datetime.now().strftime("%H%M%S")
        print(f'({date_stamp}\t{time_stamp})\t{log_type}\t|\t{log_message}')
        insert_log_to_db(date_stamp, time_stamp, log_type, log_message)


Logger.log('success', 'somemoomosm')