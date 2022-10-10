from Services.Generators.DataFrameGenerator import DataFrameGenerator
import os
from Services.load_config import Config
from Services.Generators.ParamsBuilder import ParamsBuilder


if __name__ == '__main__':
    config = Config()

    suppliers = config.get_app_suppliers()

    for supplier in suppliers:
        print(supplier)
        params = ParamsBuilder.get_supplier_params(supplier)
        print(params)
        print(DataFrameGenerator.get_supplier_dataframe(params))

