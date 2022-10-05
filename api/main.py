import time

from Services.Db import DbService
from Services.Processors import DownloadProcessor
from Services.Processors import SupplierProcessor
from Services.load_config import Config
from Services.ScriptGen.GenLoader import GenLoader
from Services.ScriptGen.ProcessorBuilder import ProcessorBuilder

if __name__ == '__main__':
    config = Config()

    # config.get_app_info()
    gen_loader = GenLoader()
    proc_builder = ProcessorBuilder()
    tmp = gen_loader.suppliers_list_loader()
    for item in tmp:
        proc_builder.supplier_param_builder(supplier=item)
    # file_proc.process_file(item)
    # config.create_app_suppliers()
    # DbService.connect()
    # DownloadProcessor.download()
    # SupplierProcessor.suppliers_to_db()
    # SupplierProcessor.suppliers_to_ftp()
    
