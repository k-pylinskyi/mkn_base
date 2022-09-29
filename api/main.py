import time

from Services.Db import DbService
from Services.Processors import DownloadProcessor
from Services.Processors import SupplierProcessor

if __name__ == '__main__':
    DbService.connect()
    DownloadProcessor.download()
    SupplierProcessor.suppliers_to_db()
    SupplierProcessor.suppliers_to_ftp()
