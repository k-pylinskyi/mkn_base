from api.SupplierScripts import *


def get_queried_data():
    hart = Hart()
    dataframes = hart.process()
    data = dataframes[0]
    cn = dataframes[1]
    cross = dataframes[2]
    deposit = dataframes[3]
    prices = dataframes[4]
    quantity = dataframes[5]
    weight = dataframes[6]

    query = '''
            SELECT DISTINCT
            24 AS supplier_id,
            data.hart_part_number, 
            data.part_number,
            data.manufacturer,
            data.part_name, 
            REPLACE(quantity.qty, '>', '') AS quantity, 
            IIF(deposit.price is null, prices.price, prices.price + ROUND(deposit.price, 2)) AS final_price,
            data.unit_measure,
            weight.weight,
            data.origin
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
            quantity.warehouse in('V', 'S', '1') 
            '''

    return sqldf(query)


class Hart:
    pd.set_option('display.max_columns', 4)

    def __init__(self):
        directory = "../TemporaryStorage//Hart//files"

        self.quantity_columns = ['hart_part_number', 'qty', 'warehouse']
        self.cn_columns = ['hart_part_number', 'tariff_code', 'weight']
        self.deposit_columns = ['hart_part_number', 'tariff_code', 'price']
        self.prices_columns = ['hart_part_number', 'price']
        self.data_columns = [
            'hart_part_number',
            'tecdoc_number',
            'manufacturer',
            'part_number',
            'part_name',
            'category',
            'unit_measure',
            'price',
            'deposit',
            'oe_number',
            'additional_numbers',
            'ean_codes',
            'origin'
        ]
        self.cross_columns = [
            'hart_part_number',
            'part_number',
            'part_name',
            'manufacturer',
            'hart_part_number_cross',
            'part_number_cross',
            'part_name_cross',
            'manufacturer_cross'
        ]
        self.weight_columns = [
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
        self.data = pd.read_csv(os.path.join(directory, 'hart_data.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.cn = pd.read_csv(os.path.join(directory, 'hart_cn.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.cross = pd.read_csv(os.path.join(directory, 'hart_cross.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.deposit = pd.read_csv(os.path.join(directory, 'hart_deposit.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.prices = pd.read_csv(os.path.join(directory, 'hart_prices.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.quantity = pd.read_csv(os.path.join(directory, 'hart_quantity.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)
        self.weight = pd.read_csv(os.path.join(directory, 'hart_weight.csv'), sep=';', skiprows=1, decimal=',', error_bad_lines=False, low_memory=False)

    def process(self):
        self.data.columns = self.data_columns
        self.data.part_number = DataFrameReader.format_column(self.data.part_number)
        self.data.drop(self.data.columns[[5, 7, 8, 9, 10]], axis=1, inplace=True)

        self.cn.columns = self.cn_columns
        self.cn.drop(self.cn.columns[[2]], axis=1, inplace=True)

        self.cross.columns = self.cross_columns
        self.cross.drop(self.cross.columns[[1, 2, 3]], axis=1, inplace=True)

        self.deposit.columns = self.deposit_columns
        self.deposit.drop(self.deposit.columns[[1]], axis=1, inplace=True)

        self.prices.columns = self.prices_columns

        self.quantity.columns = self.quantity_columns

        self.weight.columns = self.weight_columns
        self.weight.drop(self.weight.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]], axis=1, inplace=True)

        print(self.cn.head())

        return [self.data, self.cn, self.cross, self.deposit, self.prices, self.quantity, self.weight]
