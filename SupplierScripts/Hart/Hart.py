from Services.Processors.DataFrameReader import DataFrameReader as dfreader
from pandasql import sqldf
import pandas as pd


class Hart:
    def __init__(self):
        directory = "./TemporaryStorage//Hart//files"
        self.dfs_dict = dfreader.get_data_frames(directory, 1)

    def process(self):
        data = self.dfs_dict.get("hart_data")
        data.columns = ['hart_part_number', 'tecdoc_number', 'supplier', 'part_number', 'part_name', 'category', 'unit_measure', 'price', 'deposit', 'oe_number', 'additional_numbers', 'ean_codes', 'origin']

        quantity = self.dfs_dict.get("96285_Quantity")
        quantity.columns = ['hart_part_number', 'qty', 'warehouse']

        cn = self.dfs_dict.get("hart_cn")
        cn.columns = ['hart_part_number', 'tariff_code', 'weight']

        cross = self.dfs_dict.get("hart_cross")
        cross.columns = ['hart_part_number', 'part_number', 'part_name', 'supplier', 'hart_part_number_cross', 'part_name_cross', 'name_cross', 'supplier_cross']

        deposit = self.dfs_dict.get("hart_deposit")
        deposit.columns = ['hart_part_number', 'tariff_code', 'price']

        price = self.dfs_dict.get("hart_prices")
        price.columns = ['hart_part_number', 'price']

        weight = self.dfs_dict.get("hart_weight")
        weight.columns = ['hart_part_number', 'tecdoc_number', 'supplier', 'part_number', 'part_name', 'category', 'unit_measure', 'price', 'deposit', 'oe_number', 'additional_numbers', 'ean_codes', 'origin', 'weight']

        query = """
        SELECT DISTINCT
        data.hart_part_number, 
        data.part_number,
        data.supplier,
        data.part_name, 
        price.price, 
        REPLACE(quantity.qty, '>', ''), 
        quantity.warehouse,
        IFNULL(deposit.price, 0.00) as deposit,
        price.price + IFNULL(deposit.price, 0.00) as final_price,
        weight.weight,
        data.ean_codes,
        data.origin,
        data.oe_number,
        data.tecdoc_number
        FROM data 
        INNER JOIN price 
        ON data.hart_part_number = price.hart_part_number
        INNER JOIN quantity 
        ON data.hart_part_number = quantity.hart_part_number
        LEFT JOIN deposit
        ON data.hart_part_number = deposit.hart_part_number
        INNER JOIN weight
        ON data.hart_part_number = weight.hart_part_number
        WHERE 
        quantity.qty not like '0' AND
        quantity.warehouse in('V', 'S', '1')
        """

        df = sqldf(query)
        pd.options.display.max_columns = 20
        print(df)


