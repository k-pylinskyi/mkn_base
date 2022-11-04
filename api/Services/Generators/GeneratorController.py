from Services.Generators.DataFrameGenerator import DataFrameGenerator
from Services.Generators.SqlGenerator import SqlGenerator
from Services.Generators.ParamsBuilder import ParamsBuilder
from Services.Loader.LoadController import LoadController


class GeneratorController:
    @staticmethod
    def process_supplier(supplier_name):
        params = ParamsBuilder.get_supplier_params(supplier_name)
        if params['status']:
            print(params)
            download_files = params.get('download_files')
            if download_files is not None:
                for file in download_files:
                    file_name = file.get('download_file_name')
                    download_type = file.get('download_type')
                    download_params = file.get('download_params')
                    LoadController.download(download_type, supplier_name, file_name, download_params)
            df = DataFrameGenerator.get_supplier_dataframe(params)
            df = SqlGenerator.get_queried_data(df, params)
            return df
        else:
            print(f'Supplier {params["supplier_name"]} is disabled')

