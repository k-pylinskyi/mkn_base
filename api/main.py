from Services.Processors.SuppliersProcessor import *
from Services.ScriptGen.GenLoader import GenLoader
from Services.ScriptGen.ProcessorBuilder import ProcessorBuilder

if __name__ == '__main__':
    #suppliers_to_db()
     # config.get_app_info()
    gen_loader = GenLoader()
    proc_builder = ProcessorBuilder()
    tmp = gen_loader.suppliers_list_loader()
    for item in tmp:
        proc_builder.supplier_param_builder(supplier=item)
