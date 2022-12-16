from api.Services.Ftp.FtpConnection import FtpConnection
from api.Services.Db.DbService import DbService

class FtpSender:
    @staticmethod
    def send(table_name):
        db = DbService()
        print('Exporting {} to csv'.format(table_name))
        file = db.get_table_csv(table_name)
        ftp = FtpConnection('138.201.56.185', 'ph6802', 'z7lIh8iv10pLRt')
        ftp.upload_file(file, 'maxi_export', table_name)
