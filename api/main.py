from api.Services.Db import DbService
from api.Services.Processors import DownloadProcessor
from api.Services.Processors import SupplierProcessor

if __name__ == '__main__':
    DbService.connect()
    #DownloadProcessor.download()

    SupplierProcessor.suppliers_to_db()
