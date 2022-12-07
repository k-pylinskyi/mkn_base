from SupplierScripts import *

def euro_kas_to_db():
    table_name = 'euro_kas'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_euro_kas_data())
    DataFrameReader.supplier_to_ftp(table_name)

def get_euro_kas_data():
    eurokas = EuroKas()
    data = eurokas.process()

    query = '''
        SELECT
            "VOLVO" as manufacturer,
            supplier_part_number,
            supplier_part_number as part_number,
            part_name_1,
            part_name_2,
            part_name_3,
            supplier_price,
            discount_percent,
            price,
            999 as quantity,
            "PLN" as currency,
            8 as delivery
        FROM
            data
    '''

    return sqldf(query)

class EuroKas:
    def __init__(self):
        self.data_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/euro_kas/eurokas_volvo.xlsx.xlsx'
        self.columns = {
            0: 'supplier_part_number',
            1: 'part_name_1',
            2: 'part_name_2',
            3: 'part_name_3',
            4: 'discount_group',
            5: 'supplier_price',
            6: 'discount_percent',
            7: 'discount_amount',
            8: 'price'
        }

    def process(self):
        data = pd.read_excel(self.data_url, header=None, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8], skiprows=1)
        print(data.head())
        data.rename(columns=self.columns, inplace=True)
        print(data.head())

        return data
