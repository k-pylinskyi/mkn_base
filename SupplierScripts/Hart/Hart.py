from SupplierScripts.DataFrameReader import DataFrameReader as dfreader
from pandasql import sqldf

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

        query = """SELECT
        data.main_part_number,
        data.manufacturer,
        data.category,
        data.origin,
        price.price,
        IFNULL(deposit.deposit, 0) AS deposit, quantity.warehouse,
        REPLACE(quantity.quantity, '>', '') AS quantity,
        (price.price + IFNULL(deposit.deposit, 0)) AS final_price
        FROM data
        INNER JOIN price ON  data.part_number = price.part_number
        INNER JOIN quantity ON data.part_number = quantity.part_number
        LEFT JOIN deposit ON data.part_number = deposit.part_number
        WHERE
        price.price > 2
        AND (quantity.warehouse = 'A' OR quantity.warehouse = 'H' OR quantity.warehouse = 'J' OR
        quantity.warehouse = '3' OR quantity.warehouse = '9')
        AND (price.price + IFNULL(deposit.deposit, 0)) > 2;"""


