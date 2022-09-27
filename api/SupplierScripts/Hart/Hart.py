from api.SupplierScripts import *


def hart_to_db():
    print('Pushing Hart to Data Base')
    DataFrameReader.dataframe_to_db('hart', get_hart_data())


def get_hart_data():
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
            data.manufacturer,
            data.hart_part_number as supplier_part_number, 
            data.part_number,
            data.part_name, 
            REPLACE(quantity.qty, '>', '') AS quantity, 
            IIF(deposit.price is null, prices.price, prices.price + ROUND(deposit.price, 2)) AS price,
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

    def __init__(self):
        directory = "../TemporaryStorage//Hart//files"

        self.quantity_columns = {0: 'hart_part_number', 1: 'qty', 2: 'warehouse'}
        self.cn_columns = {0: 'hart_part_number', 1: 'tariff_code'}
        self.deposit_columns = {0: 'hart_part_number', 2: 'price'}
        self.prices_columns = {0: 'hart_part_number', 1: 'price'}
        self.weight_columns = {0: 'hart_part_number', 13: 'weight'}
        self.data_columns = {
            0: 'hart_part_number', 1: 'tecdoc_number', 2: 'manufacturer', 3: 'part_number',
            4: 'part_name', 6: 'unit_measure', 11: 'ean_codes', 12: 'origin'
        }
        self.cross_columns = {
            0: 'hart_part_number', 4: 'hart_part_number_cross', 5: 'part_number_cross',
            6: 'part_name_cross', 7: 'manufacturer_cross'
        }
        self.data = pd.read_csv(os.path.join(directory, 'hart_data.csv'), sep=';',
                                header=None, skiprows=1, decimal=',', usecols=[0, 1, 2, 3, 4, 6, 11, 12])
        self.cn = pd.read_csv(os.path.join(directory, 'hart_cn.csv'), sep=';',
                              header=None, skiprows=1, decimal=',', usecols=[0, 1])
        self.cross = pd.read_csv(os.path.join(directory, 'hart_cross.csv'), sep=';',
                                 header=None, skiprows=1, decimal=',', usecols=[0, 4, 5, 6, 7])
        self.deposit = pd.read_csv(os.path.join(directory, 'hart_deposit.csv'), sep=';',
                                   header=None, skiprows=1, decimal=',', usecols=[0, 2])
        self.prices = pd.read_csv(os.path.join(directory, 'hart_prices.csv'), sep=';',
                                  header=None, skiprows=1, decimal=',')
        self.quantity = pd.read_csv(os.path.join(directory, 'hart_quantity.csv'), sep=';',
                                    header=None, decimal=',')
        self.weight = pd.read_csv(os.path.join(directory, 'hart_weight.csv'), sep=';',
                                  header=None, skiprows=1, decimal=',', usecols=[0, 13])

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        self.cn.rename(columns=self.cn_columns, inplace=True)
        self.cross.rename(columns=self.cross_columns, inplace=True)
        self.deposit.rename(columns=self.deposit_columns, inplace=True)
        self.prices.rename(columns= self.prices_columns, inplace=True)
        self.quantity.rename(columns=self.quantity_columns, inplace=True)
        self.weight.rename(columns=self.weight_columns, inplace=True)

        return [self.data, self.cn, self.cross, self.deposit, self.prices, self.quantity, self.weight]
