import time

from Services.Db import DbService
from Services.Processors import DownloadProcessor
from Services.Processors import SupplierProcessor
from Services.load_config import Config

if __name__ == '__main__':
    config = Config()

    config.get_app_info()
    # config.get_app_suppliers()
    # config.create_app_suppliers()
    DbService.connect()
    # DownloadProcessor.download()
    SupplierProcessor.suppliers_to_db()
    SupplierProcessor.suppliers_to_ftp()
    
