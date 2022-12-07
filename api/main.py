from runner import Runner
from Services.Db.DbService import DbService

if __name__ == '__main__':
    Runner.run()
    DbService.get_db_backup()
