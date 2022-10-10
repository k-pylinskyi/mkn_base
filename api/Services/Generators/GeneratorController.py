from Services.Generators.DataFrameGenerator import DataFrameGenerator
from Services.Generators.SqlGenerator import SqlGenerator
from Services.Generators.ParamsBuilder import ParamsBuilder
from Services.load_config import Config


class GeneratorController:
    @staticmethod
    def process_suppliers_from_config(config=Config()):
        suppliers = config.get_app_suppliers()
        for supplier_name in suppliers:
            params = ParamsBuilder.get_supplier_params(supplier_name)
            if params['status']:
                print(params)
                df = DataFrameGenerator.get_supplier_dataframe(params)
                df = SqlGenerator.get_queried_data(df, params)
                print(df)
            else:
                print(f'Supplier {params["supplier_name"]} is disabled')

