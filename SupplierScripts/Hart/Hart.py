from Services.Processors.DataFrameReader import DataFrameReader as dfreader


class Hart:
    def __init__(self):
        directory = "./TemporaryStorage//Hart//files"
        self.dfs_dict = dfreader.get_data_frames(directory)

    def process(self):
        data = self.dfs_dict.get("hart_data")
        data.columns = ['hart_part_number', 'tecdoc_number', 'part_number', 'part_name', 'unit_measure', 'price', 'deposit', 'oe_number', 'additional_numbers', 'ean_codes', 'origin']

        quantity = self.dfs_dict.get("96285_Quantity")
        quantity.columns = ['hart_part_number', 'qty', 'warehouse']

        cn = self.dfs_dict.get("hart_cn")
        cn.columns = ['hart_part_number', 'tariff_code', 'weight']

        cross = self.dfs_dict.get("hart_cross")
        cross.columns = ['hart_part_number', 'part_number', 'part_name', 'hart_part_number_cross', 'part_name_cross', 'supplier_cross']

        deposit = self.dfs_dict.get("hart_deposit")
        deposit.columns = []

        price = self.dfs_dict.get("hart_price")

        weight = self.dfs_dict.get("hart_weight")




