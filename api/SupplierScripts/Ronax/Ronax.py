from SupplierScripts import *

def ronax_to_db():
    table_name = 'ronax'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_ronax_data()
    DataFrameReader.dataframe_to_db(table_name, data)

def get_ronax_data():
    ronax = Ronax()
    dfs = []
    for df in ronax.process():
        df['part_number'] = df['supplier_part_number']
        df['quantity'] = 999
        dfs.append(df)

    return pd.concat(dfs, ignore_index=False)

class Ronax:
    def __init__(self):
        self.vag_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/ronax/VAG.csv'
        self.toyota_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/ronax/Toyota.csv'
        self.bmw_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/ronax/BMW.csv'
        self.renault_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/ronax/Renault.csv'

        self.columns = {
            0: 'supplier_part_number',
            1: 'price'
        }

    def process(self):
        vag = pd.read_csv(self.vag_url, sep=';', header=None, skiprows=2, usecols=[0, 1], decimal=',')
        vag.rename(columns=self.columns, inplace=True)
        vag['manufacturer'] = 'VAG'
        vag['delivery'] = 10
        vag.supplier_part_number = vag.supplier_part_number.str.replace('=', '')
        vag.supplier_part_number = vag.supplier_part_number.str.replace('"', "")
        toyota = pd.read_csv(self.toyota_url, sep=';', header=None, skiprows=2, usecols=[0, 1], decimal=',')
        toyota.rename(columns=self.columns, inplace=True)
        toyota['manufacturer'] = 'TOYOTA'
        toyota['delivery'] = 9
        toyota.supplier_part_number = toyota.supplier_part_number.str.replace('=', '')
        toyota.supplier_part_number = toyota.supplier_part_number.str.replace('"', "")
        bmw = pd.read_csv(self.bmw_url, sep=';', header=None, skiprows=2, usecols=[0, 1], decimal=',')
        bmw.rename(columns=self.columns, inplace=True)
        bmw['manufacturer'] = 'BMW'
        bmw['delivery'] = 14
        bmw.supplier_part_number = bmw.supplier_part_number.str.replace('=', '')
        bmw.supplier_part_number = bmw.supplier_part_number.str.replace('"', "")
        renault = pd.read_csv(self.renault_url, sep=';', header=None, skiprows=2, usecols=[0, 1], decimal=',')
        renault.rename(columns=self.columns, inplace=True)
        renault['manufacturer'] = 'RENAULT'
        renault['delivery'] = 9
        renault.supplier_part_number = renault.supplier_part_number.str.replace('=', '')
        renault.supplier_part_number = renault.supplier_part_number.str.replace('"', "")

        return [vag, toyota, bmw, renault]

