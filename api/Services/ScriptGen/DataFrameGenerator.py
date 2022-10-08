import pandas as pd
from Services.ScriptGen.ParamsBuilder import ParamsBuilder
from Services.load_config import Config


class DataFrameGenerator:
    @classmethod
    def get_supplier_dataframes(cls, params):
        supplier_name = params['supplier_name']
        if params['status']:
            print(f'Getting {supplier_name} data frames')
            files = params['files']
            dfs = []
            for file_params in files:
                df = DataFrameGenerator.get_dataframe(file_params)
                dfs.append(df)
            return dfs
        else:
            print(f'Supplier {supplier_name} is disabled')

    @classmethod
    def get_dataframe(cls, params):
        print(f"\tFile: {params['file_name']}")
        if params['file_type'] == 'csv':
            return pd.read_csv(
                filepath_or_buffer=params['filepath_or_buffer'],
                sep=params['sep'],
                decimal=params['decimal'],
                skiprows=params['skip_rows'],
                header=params['header'],
                compression=params['compression'],
                low_memory=params['low_memory'],
                encoding_errors=params['encoding_errors'],
                encoding=params['encoding'],
                engine=params['engine'],
                error_bad_lines=params['error_bad_lines'],
                on_bad_lines=params['on_bad_lines'],
                usecols=params['use_cols'],
            )
        elif params['file_type'] == 'excel':
            return pd.read_excel(
                io=params['filepath_or_buffer'],
                decimal=params['decimal'],
                header=params['header'],
                engine=params['engine'],
                skiprows=params['skip_rows']
            )
        else:
            return

    @staticmethod
    def process_suppliers_from_config(config = Config()):
        suppliers = config.get_app_suppliers()
        for supplier in suppliers:
            params = ParamsBuilder.get_supplier_params(supplier)
            dfs = DataFrameGenerator.get_supplier_dataframes(params)
            print(dfs)
