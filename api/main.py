import time

from Services.Db import DbService
from Services.Processors import DownloadProcessor
from Services.Processors import SupplierProcessor
from SupplierScripts.Intervito.Intervito import *

if __name__ == '__main__':
    #DbService.connect()
    #DownloadProcessor.download()
    SupplierProcessor.suppliers_to_db()
    SupplierProcessor.suppliers_to_ftp()
