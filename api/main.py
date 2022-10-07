from Services.Processors.SuppliersProcessor import *
from Services.ScriptGen.GenLoader import GenLoader
from Services.ScriptGen.ProcessorBuilder import ProcessorBuilder
from Services.load_config import Config
from Services.edit_config import *

if __name__ == '__main__':
    suppliers_to_db()
    # config = Config()
    # change_supplier_activity(config=config, supplier='autoland', status=False)

    # config.get_app_info()
    # gen_loader = GenLoader()
    # proc_builder = ProcessorBuilder()
    # tmp = gen_loader.suppliers_list_loader()
    # for item in tmp:
    #     proc_builder.supplier_param_builder(supplier=item)
