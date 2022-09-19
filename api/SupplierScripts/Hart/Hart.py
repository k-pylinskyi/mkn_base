from pandasql import sqldf

from api.Services.Db.DbContext import DbContext
from api.Services.Processors.DataFrameReader import DataFrameReader as DataFrameReader


class Hart:
    def __init__(self):
        directory = "./TemporaryStorage//Hart//files"
        self.dfs_dict = DataFrameReader.get_data_frames(directory, ',', 1)

    def process(self):
        data = self.dfs_dict.get("hart_data")
        data.columns = ['hart_part_number', 'tecdoc_number', 'supplier', 'part_number', 'part_name', 'category',
                        'unit_measure', 'price', 'deposit', 'oe_number', 'additional_numbers', 'ean_codes', 'origin']
        data['part_number'] = DataFrameReader.format_column(data['part_number'])

        quantity = self.dfs_dict.get("96285_Quantity")
        quantity.columns = ['hart_part_number', 'qty', 'warehouse']

        cn = self.dfs_dict.get("hart_cn")
        cn.columns = ['hart_part_number', 'tariff_code', 'weight']

        cross = self.dfs_dict.get("hart_cross")
        cross.columns = ['hart_part_number', 'part_number', 'part_name', 'supplier', 'hart_part_number_cross',
                         'part_name_cross', 'name_cross', 'supplier_cross']

        deposit = self.dfs_dict.get("hart_deposit")
        deposit.columns = ['hart_part_number', 'tariff_code', 'price']

        price = self.dfs_dict.get("hart_prices")
        price.columns = ['hart_part_number', 'price']

        weight = self.dfs_dict.get("hart_weight")
        weight.columns = ['hart_part_number', 'tecdoc_number', 'supplier', 'part_number', 'part_name', 'category','unit_measure', 'price', 'deposit', 'oe_number', 'additional_numbers', 'ean_codes', 'origin', 'weight']

        query = """
        SELECT DISTINCT
        24 as supplier_id,
        data.hart_part_number as supplier_part_number, 
        data.part_number,
        data.supplier as manufacturer,
        data.part_name, 
        REPLACE(quantity.qty, '>', '') as quantity, 
        IIF(deposit.price is null, price.price, price.price + ROUND(deposit.price, 2)) as mnk_price
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
        quantity.qty not like '0' 
        AND
        quantity.warehouse in('V', 'S', '1') 
        """

        return sqldf(query)

    def to_db(self, table_name):
        context = DbContext()
        connection = context.db
        df = self.process()
        df.to_sql(table_name, connection, if_exists='replace', index=False)
