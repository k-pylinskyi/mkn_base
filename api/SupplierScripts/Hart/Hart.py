import pandas as pd
from pandasql import sqldf
import os

from api.Services.Db.DbContext import DbContext
from api.Services.Processors.DataFrameReader import DataFrameReader as DataFrameReader


class Hart:
    def __init__(self):
        directory = "../TemporaryStorage//Hart//files"
        self.data = pd.read_csv(os.path.join(directory, 'hart_data.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.cn = pd.read_csv(os.path.join(directory, 'hart_cn.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.cross = pd.read_csv(os.path.join(directory, 'hart_cross.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.deposit = pd.read_csv(os.path.join(directory, 'hart_deposit.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.prices = pd.read_csv(os.path.join(directory, 'hart_prices.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.quantity = pd.read_csv(os.path.join(directory, 'hart_quantity.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.weight = pd.read_csv(os.path.join(directory, 'hart_weight.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)


    def process(self):
        self.data.columns = [
            'hart_part_number',
            'tecdoc_number',
            'supplier',
            'part_number',
            'part_name',
            'category',
            'unit_measure',
            'price', 'deposit',
            'oe_number',
            'additional_numbers',
            'ean_codes',
            'origin'
        ]
        self.data['part_number'] = DataFrameReader.format_column(self.data['part_number'])

        self.quantity.columns = [
            'hart_part_number',
            'qty',
            'warehouse'
        ]

        self.cn.columns = [
            'hart_part_number',
            'tariff_code',
            'weight'
        ]

        self.cross.columns = [
            'hart_part_number',
            'part_number',
            'part_name',
            'supplier',
            'hart_part_number_cross',
            'part_name_cross',
            'name_cross',
            'supplier_cross'
        ]

        self.deposit.columns = [
            'hart_part_number',
            'tariff_code',
            'price'
        ]

        self.prices.columns = [
            'hart_part_number',
            'price'
        ]

        self.weight.columns = [
            'hart_part_number',
            'tecdoc_number',
            'supplier',
            'part_number',
            'part_name',
            'category',
            'unit_measure',
            'price',
            'deposit',
            'oe_number',
            'additional_numbers',
            'ean_codes',
            'origin',
            'weight'
        ]

        query = """
        SELECT DISTINCT
        24 as supplier_id,
        data.hart_part_number as supplier_part_number, 
        data.part_number,
        data.supplier as manufacturer,
        data.part_name, 
        REPLACE(quantity.qty, '>', '') as quantity, 
        IIF(deposit.price is null, prices.price, prices.price + ROUND(deposit.price, 2)) as mnk_price
        FROM data 
        INNER JOIN prices 
        ON data.hart_part_number = prices.hart_part_number
        INNER JOIN quantity 
        ON data.hart_part_number = quantity.hart_part_number
        LEFT JOIN deposit
        ON data.hart_part_number = deposit.hart_part_number
        INNER JOIN weight
        ON data.hart_part_number = weight.hart_part_number
        WHERE 
        quantity.qty not like '0' 
        AND
        quantity.warehouse in('V', 'S', '1') 
        """

        return sqldf(query)